"""Hybrid Search combining Sparse BM25 and Dense Retrieval via Reciprocal Rank Fusion (RRF)."""
from typing import List, Dict, Any
from .bm25 import BM25Retriever


class HybridSearchEngine:
    """Executes dense and sparse searches and fuses ranking positions using RRF."""

    def __init__(self, documents: List[Dict[str, Any]], rrf_k: int = 60):
        self.documents = documents
        self.rrf_k = rrf_k
        self.bm25 = BM25Retriever()
        self.bm25.fit(documents)

    def _dense_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # Mock dense semantic similarity via token overlap
        tokens = set(query.lower().split())
        scored = []
        for doc in self.documents:
            doc_tokens = set(doc["content"].lower().split())
            score = len(tokens.intersection(doc_tokens)) / max(1, len(tokens))
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:top_k]]

    def search(self, query: str, top_n: int = 3) -> List[Dict[str, Any]]:
        sparse_hits = self.bm25.search(query, top_k=5)
        dense_hits = self._dense_search(query, top_k=5)

        # Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[str, float] = {}
        doc_map: Dict[str, Dict[str, Any]] = {}

        for rank, doc in enumerate(sparse_hits, 1):
            doc_id = doc["id"]
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank))

        for rank, doc in enumerate(dense_hits, 1):
            doc_id = doc["id"]
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank))

        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [{"rrf_score": round(score, 6), **doc_map[did]} for did, score in sorted_docs[:top_n]]
