"""RocketRide implementation of the rag_qa workload — runs the equivalent .pipe pipeline.

Contract: run_once(payload) -> {"model_ms": float, "output": str}
Uses the RocketRide SDK to execute workloads/rag_qa/rag_qa.pipe against ROCKETRIDE_URI.
Keep the model, prompt, and inputs IDENTICAL to the LangChain implementation.
"""
import os, time

def run_once(payload):
    # TODO:
    #   from rocketride import Client
    #   client = Client(uri=os.getenv("ROCKETRIDE_URI"), auth=os.getenv("ROCKETRIDE_AUTH"))
    #   result = client.run("workloads/rag_qa/rag_qa.pipe", inputs={...})
    # Capture the model node's reported time for model_ms via observability if available.
    raise NotImplementedError(
        "Wire the RocketRide SDK + rag_qa.pipe here. Return {'model_ms': <llm time ms>, 'output': <answer>}."
    )
