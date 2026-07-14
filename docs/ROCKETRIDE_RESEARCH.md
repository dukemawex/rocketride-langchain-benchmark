# RocketRide — Research Brief

Sourced from the official site, GitHub, and launch discussion (Jul 2026).

## What it is
RocketRide is an open-source **AI/data pipeline engine** — an "AI Development Environment" — that builds and runs LLM/data pipelines from inside your IDE. You compose pipelines visually on a VS Code canvas; they're stored as portable JSON `.pipe` files and executed by a **multithreaded C++ runtime**.

- Sites: https://rocketride.org · Cloud: https://cloud.rocketride.ai · Docs: https://docs.rocketride.org
- GitHub: https://github.com/rocketride-org/rocketride-server (MIT)
- SDKs: Python (`pip install rocketride`), TypeScript (`npm i rocketride`), MCP server
- Launched ~mid-2026; self-described as young ("two weeks post-launch... rough around the edges, but the core engine is solid").

## Architecture
- **C++ core, native multithreading** — built for throughput on AI/data workloads.
- **85+ nodes**: 13 LLM providers, 8 vector DBs, OCR, NER, PII anonymization, chunking, embeddings; nodes are Python-extensible.
- **Multi-agent**: built-in CrewAI **and LangChain** support (relevant — the benchmark may pit LangChain-in-Python vs LangChain-orchestrated-by-RocketRide, or vs native RocketRide nodes; clarify with client).
- **Deploy**: Docker / on-prem / local process, or **RocketRide Cloud** (managed, "now live", patent-pending model server claimed to cut cost). Same `.pipe` runs unchanged across all.
- Observability: call-tree tracing, token usage, latency, memory per run.

## Positioning vs LangChain
- LangChain = Python framework; incurs per-step framework overhead and needs manual optimization (caching, async, batching) for production throughput.
- RocketRide's pitch = C++ engine + visual builder + on-your-infra + observability, aimed at production performance and lower ops.
- **No public, independent head-to-head benchmark exists** — which is exactly the gap this gig fills.

## Benchmark implications / questions for the client
1. Is the comparison **LangChain (Python) vs RocketRide native nodes**, or **LangChain-in-Python vs LangChain-orchestrated-by-RocketRide**? Changes the workload build.
2. Cloud, on-prem, or both? (Cloud vs local isn't like-for-like hardware.)
3. Which model/provider to pin? Local model would remove network variance.
4. Target workload shape: RAG, multi-step agent, or high-throughput batch (batch favors a C++/multithreaded engine most).
5. What's the success metric they care about — latency, throughput, cost, or ops simplicity?

## Sources
- https://github.com/rocketride-org/rocketride-server/blob/develop/README.md
- https://news.ycombinator.com/item?id=47415771
- https://cloud.rocketride.ai/
