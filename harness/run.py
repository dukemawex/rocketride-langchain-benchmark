#!/usr/bin/env python3
"""Benchmark runner: times a workload on a chosen engine, samples resources, writes JSONL.

Usage:
  python harness/run.py --workload rag_qa --engine langchain --runs 50 --concurrency 4
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse, json, time, importlib, statistics, os, sys, platform
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

try:
    import psutil
except ImportError:
    psutil = None


def load_engine(engine, workload):
    """Import benchmarks.<engine>.<workload> which must expose run_once(payload)->dict."""
    mod = importlib.import_module(f"benchmarks.{engine}.{workload}")
    return mod.run_once


def env_info():
    return {
        "os": platform.platform(),
        "python": platform.python_version(),
        "cpu": platform.processor() or platform.machine(),
        "model": os.getenv("BENCH_MODEL", "unset"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", required=True)
    ap.add_argument("--engine", required=True, choices=["langchain", "rocketride"])
    ap.add_argument("--runs", type=int, default=50)
    ap.add_argument("--warmup", type=int, default=5)
    ap.add_argument("--concurrency", type=int, default=1)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    try:
        run_once = load_engine(args.engine, args.workload)
    except ModuleNotFoundError as e:
        print(f"[stub] engine/workload not implemented yet: {e}", file=sys.stderr)
        print("       Implement benchmarks/%s/%s.py with run_once(payload)->{'model_ms':..,'output':..}" %
              (args.engine, args.workload), file=sys.stderr)
        sys.exit(2)

    payload = {"workload": args.workload}
    # probe: detect not-yet-implemented workloads cleanly
    try:
        run_once(payload)
    except NotImplementedError as e:
        print(f"[stub] {args.engine}/{args.workload} not implemented yet: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception:
        pass  # real runtime errors (e.g. missing keys) surface during timed runs
    # warm-up
    for _ in range(args.warmup):
        try: run_once(payload)
        except Exception: pass

    latencies, records = [], []
    proc = psutil.Process() if psutil else None
    peak_rss = 0

    def timed_call(_):
        t0 = time.perf_counter()
        r = run_once(payload)
        dt = (time.perf_counter() - t0) * 1000.0
        return dt, r

    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        for dt, r in ex.map(timed_call, range(args.runs)):
            latencies.append(dt)
            model_ms = (r or {}).get("model_ms")
            records.append({"e2e_ms": dt, "model_ms": model_ms,
                            "overhead_ms": (dt - model_ms) if model_ms is not None else None})
            if proc:
                peak_rss = max(peak_rss, proc.memory_info().rss)

    latencies.sort()
    def pct(p): return latencies[min(len(latencies) - 1, int(len(latencies) * p))]
    summary = {
        "engine": args.engine, "workload": args.workload,
        "runs": args.runs, "concurrency": args.concurrency,
        "p50_ms": round(pct(0.50), 2), "p95_ms": round(pct(0.95), 2), "p99_ms": round(pct(0.99), 2),
        "mean_ms": round(statistics.mean(latencies), 2),
        "throughput_rps": round(args.runs / (sum(latencies) / 1000.0 / args.concurrency), 2),
        "peak_rss_mb": round(peak_rss / 1e6, 1) if peak_rss else None,
        "env": env_info(), "ts": datetime.now(timezone.utc).isoformat(),
    }

    out = args.out or f"results/{args.engine}_{args.workload}_c{args.concurrency}.jsonl"
    os.makedirs("results", exist_ok=True)
    with open(out, "w") as f:
        f.write(json.dumps({"summary": summary}) + "\n")
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
