#!/usr/bin/env python3
"""Aggregate JSONL result files into a comparison table (and optional HTML)."""
import sys, json, glob

def load(path):
    with open(path) as f:
        first = f.readline()
    return json.loads(first).get("summary")

def main():
    paths = []
    for a in sys.argv[1:]:
        paths.extend(glob.glob(a))
    rows = [load(p) for p in paths if load(p)]
    if not rows:
        print("No result summaries found. Run harness/run.py first."); return
    cols = ["engine","workload","concurrency","p50_ms","p95_ms","p99_ms","throughput_rps","peak_rss_mb"]
    w = {c: max(len(c), *(len(str(r.get(c,''))) for r in rows)) for c in cols}
    line = " | ".join(c.ljust(w[c]) for c in cols)
    print(line); print("-" * len(line))
    for r in sorted(rows, key=lambda x: (x["workload"], x["engine"], x["concurrency"])):
        print(" | ".join(str(r.get(c,"")).ljust(w[c]) for c in cols))

if __name__ == "__main__":
    main()
