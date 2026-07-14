# Benchmark Methodology

The goal is an **apples-to-apples, reproducible** comparison of the RocketRide runtime vs LangChain on identical workloads. Neutral by design.

## 1. Fairness controls
- **Identical workload**: same task, prompts, documents, and model for both stacks. The only variable is the orchestration runtime.
- **Same model + provider**: pin one model (e.g. `gpt-4o-mini`) and the same provider endpoint for both. Optionally add a local model to remove network variance entirely.
- **Same hardware**: LangChain baseline and RocketRide on-prem engine run on the same machine. RocketRide Cloud is measured separately and clearly labeled (managed infra ≠ local).
- **Isolate model latency**: record provider round-trip time per call. Report both end-to-end latency and **orchestration overhead = end-to-end − model time**, so we compare the runtimes rather than the LLM provider.
- **Deterministic inputs**: fixed seed, temperature 0 where supported, frozen input set committed to the repo.

## 2. Execution protocol
- Discard the first K warm-up runs (default 5).
- Run N timed repetitions (default 50) per workload per engine.
- Sweep concurrency levels (1, 4, 16) to measure throughput scaling.
- Sample CPU and peak RSS during runs.
- Record cold-start separately (first request after process start).

## 3. Metrics
End-to-end latency (p50/p95/p99), throughput (req/s), orchestration overhead, CPU %, peak memory, cold start, cost per 1k runs, and output parity (do both stacks produce equivalent answers?).

## 4. Environment capture (recorded with every run)
OS/kernel, CPU model + core count, RAM, Python version, exact `langchain*` versions, RocketRide runtime version, model name, provider, region, and git commit of this repo.

## 5. Statistics
Report percentiles not just means. Include run-to-run variance and note any outliers with likely cause (rate limits, GC, network). No cherry-picking.

## 6. Reporting
- Raw per-run data as JSONL in `results/`.
- A generated summary (table + charts) via `harness/report.py`.
- A short written findings doc: what was faster, by how much, where each stack shines, and honest caveats. Published unchanged whether or not RocketRide wins.

## 7. Threats to validity (stated up front)
- Cloud vs local is not a like-for-like hardware comparison — labeled as such.
- LLM provider variance can dominate; mitigated by isolating model time and optionally using a local model.
- A rough-around-the-edges young runtime may improve fast; version is pinned and dated.
