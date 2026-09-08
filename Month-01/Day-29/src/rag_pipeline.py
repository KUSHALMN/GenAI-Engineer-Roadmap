from typing import List, Dict, Any

try:
    from .semantic_cache import SemanticCache
    from .reranker import CrossEncoderReranker
except ImportError:
    from semantic_cache import SemanticCache
    from reranker import CrossEncoderReranker

class OptimizedRAGPipeline:
    KNOWLEDGE_BASE = [
        {"id": "doc-1", "title": "Vector Indexing", "content": "HNSW (Hierarchical Navigable Small World) graphs provide sub-millisecond approximate nearest neighbor search."},
        {"id": "doc-2", "title": "Reranking in RAG", "content": "Cross-Encoder rerankers analyze the complete query-document pair with self-attention, vastly outperforming bi-encoder embeddings in ranking precision."},
        {"id": "doc-3", "title": "Semantic Caching", "content": "Semantic caching reduces API costs and tail latency by serving semantically identical past questions without calling the LLM backend."}
    ]

    def __init__(self):
        self.cache = SemanticCache(similarity_threshold=0.85)
        self.reranker = CrossEncoderReranker()

    def query(self, user_query: str) -> Dict[str, Any]:
        cached = self.cache.get(user_query)
        if cached:
            response, sim = cached
            return {"source": "semantic_cache", "similarity": sim, "answer": response, "citations": []}

        candidates = list(self.KNOWLEDGE_BASE)
        reranked = self.reranker.rerank(user_query, candidates, top_k=2)
        answer = f"Synthesized answer: {reranked[0]['content']}"
        self.cache.set(user_query, answer)
        return {
            "source": "rag_pipeline",
            "reranked_chunks": reranked,
            "answer": answer,
            "citations": [d["id"] for d in reranked]
        }
