import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app, pipeline
from semantic_cache import SemanticCache
from reranker import CrossEncoderReranker

client = TestClient(app)

def test_cache():
    c = SemanticCache(0.8)
    c.set("What is RAG?", "RAG stands for Retrieval-Augmented Generation.")
    res = c.get("what is rag")
    assert res is not None
    assert "Retrieval-Augmented" in res[0]

def test_reranker():
    docs = [
        {"id": "1", "content": "Bananas are yellow fruit."},
        {"id": "2", "content": "Reranking improves RAG precision."}
    ]
    reranked = CrossEncoderReranker.rerank("rag reranking", docs, top_k=1)
    assert reranked[0]["id"] == "2"

def test_api_pipeline():
    pipeline.cache.clear()
    r1 = client.post("/api/v1/rag/query", json={"query": "Explain semantic caching"})
    assert r1.status_code == 200
    assert r1.json()["source"] == "rag_pipeline"

    r2 = client.post("/api/v1/rag/query", json={"query": "Explain semantic caching"})
    assert r2.status_code == 200
    assert r2.json()["source"] == "semantic_cache"
