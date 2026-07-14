# RocketRide vs LangChain — Independent Benchmark

An **independent, reproducible** benchmark comparing the [RocketRide](https://cloud.rocketride.ai/) runtime (multithreaded C++ engine, `.pipe` pipelines) against an equivalent **LangChain** (Python) implementation on a defined workload. Honest results either way.

> Status: scaffold. Awaiting the client's benchmark spec + cloud credits. The harness, workloads, and both implementations are stubbed so the spec drops straight in.

## Why this design is fair
- **Same workload, same models, same inputs** run through both stacks.
- **Same machine** for the LangChain baseline and the on-prem RocketRide engine; Cloud measured separately and labeled.
- **Warm-up runs discarded**, N repetitions, report p50/p95/p99 — not a single lucky run.
- **LLM latency isolated** from framework/orchestration overhead so we compare the *runtimes*, not the model provider.
- Every number is reproducible from this repo with one command.

## What we measure
| Metric | Why it matters |
|---|---|
| End-to-end latency (p50/p95/p99) | Real user-facing performance |
| Throughput (req/s at fixed concurrency) | Production scale |
| Orchestration overhead (total − LLM time) | The runtime's own cost |
| CPU / peak memory | Cost efficiency & density |
| Cold start | Time-to-first-response |
| Cost per 1k runs | $ at scale |
| Correctness / output parity | Honest = same answers |

## Layout
```
workloads/          # Defined tasks (RAG, multi-step agent, batch) — spec goes here
benchmarks/langchain/   # LangChain implementation of each workload
benchmarks/rocketride/  # .pipe pipelines + SDK runner for the same workloads
harness/            # Runner: timing, concurrency, resource sampling, stats
results/            # Generated reports (git-ignored except templates)
```

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add model keys + ROCKETRIDE_URI / ROCKETRIDE_AUTH
python harness/run.py --workload rag_qa --engine langchain --runs 50 --concurrency 4
python harness/run.py --workload rag_qa --engine rocketride --runs 50 --concurrency 4
python harness/report.py results/*.jsonl
```

## Methodology
See [`METHODOLOGY.md`](./METHODOLOGY.md) for the full protocol (environment pinning, fairness controls, statistics, and how findings are reported).

## Author
Emmanuel Effiom Duke — [duker.me](https://duker.me) · [github.com/dukemawex](https://github.com/dukemawex)

MIT licensed. Results published unmodified, favorable or not.
