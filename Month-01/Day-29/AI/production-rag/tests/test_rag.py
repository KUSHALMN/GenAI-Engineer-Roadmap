import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app, pipeline
from semantic_cache import SemanticCache
from reranker import CrossEncoderReranker

client = TestClient(app)

def test_semantic_cache_hit_and_miss():
    cache = SemanticCache(similarity_threshold=0.8)
    cache.set("How does HNSW index work?", "HNSW uses multi-layer graph skip-lists.")

    # High similarity hit
    hit = cache.get("how does hnsw indexing work?")
    assert hit is not None
    ans, sim = hit
    assert "skip-lists" in ans
    assert sim >= 0.8

    # Low similarity miss
    miss = cache.get("What is quantum computing?")
    assert miss is None

def test_reranker_relevance():
    candidates = [
        {"id": "doc-a", "content": "The weather in Seattle is rainy in November."},
        {"id": "doc-b", "content": "Cross encoder reranker models improve retrieval precision significantly."}
    ]
    reranked = CrossEncoderReranker.rerank("cross encoder reranking", candidates, top_k=1)
    assert len(reranked) == 1
    assert reranked[0]["id"] == "doc-b"

def test_pipeline_e2e():
    pipeline.cache.clear()
    res1 = client.post("/api/v1/rag/query", json={"query": "Explain cross encoder reranking in RAG"})
    assert res1.status_code == 200
    d1 = res1.json()
    assert d1["source"] == "rag_pipeline"
    assert len(d1["citations"]) > 0

    # Second query should hit semantic cache
    res2 = client.post("/api/v1/rag/query", json={"query": "Explain cross encoder reranking in RAG"})
    assert res2.status_code == 200
    d2 = res2.json()
    assert d2["source"] == "semantic_cache"
