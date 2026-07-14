# Workloads

Each workload is a defined, identical task run through both stacks. The **client's benchmark spec drops in here** — until then these are representative placeholders covering the common shapes.

## rag_qa — Retrieval-augmented Q&A
Embed a fixed document set → retrieve top-k → answer a fixed question set. Tests vector-DB + LLM orchestration. Stresses per-step overhead.

## agent_multistep — Multi-step tool-using agent
An agent that must call ≥3 tools in sequence to reach an answer. Tests control-flow, tool mediation, and reasoning-loop overhead.

## batch_extract — High-throughput batch extraction
Run structured extraction (e.g. NER/PII) over N documents at concurrency. Tests raw throughput and multithreading — where a C++ engine should shine.

Each folder should define: inputs (frozen), expected-output checker, and the parameters (k, doc count, tool list). Keep inputs committed so runs are reproducible.
