"""LangChain implementation of the rag_qa workload.

Contract: run_once(payload) -> {"model_ms": float, "output": str}
Fill in with a real LangChain RAG chain once the client's spec + docs are provided.
Keep the model, prompt, and inputs IDENTICAL to the RocketRide implementation.
"""
import os, time

def run_once(payload):
    # TODO: build once at import time, reuse here:
    #   from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    #   from langchain_community.vectorstores import FAISS
    #   retriever = FAISS...as_retriever(k=4); chain = prompt | ChatOpenAI(model=os.getenv("BENCH_MODEL"))
    # Measure ONLY the model call for model_ms so overhead can be isolated.
    raise NotImplementedError(
        "Implement the LangChain RAG chain here. Return {'model_ms': <llm round-trip ms>, 'output': <answer>}."
    )
