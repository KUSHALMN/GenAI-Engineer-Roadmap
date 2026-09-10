from __future__ import annotations

from typing import Any, Dict, List
from app.loader import Document
from retrieval.keyword_retriever import KeywordRetriever
from retrieval.semantic_retriever import SemanticRetriever


class HybridRetriever:
    """Combines Semantic Vector search and BM25 Keyword search with Reciprocal Rank Fusion (RRF)."""

    def __init__(
        self,
        semantic_retriever: SemanticRetriever | None = None,
        keyword_retriever: KeywordRetriever | None = None,
        rrf_k: int = 60,
    ):
        self.semantic = semantic_retriever or SemanticRetriever()
        self.keyword = keyword_retriever or KeywordRetriever()
        self.rrf_k = rrf_k

    def index(self, documents: List[Document]) -> None:
        """Index documents in both semantic and keyword indices."""
        self.semantic.index(documents)
        self.keyword.index(documents)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        semantic_weight: float = 0.5,
        keyword_weight: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """Perform hybrid retrieval aggregating results via weighted RRF."""
        # Retrieve extra candidates from each
        candidate_k = max(top_k * 2, 10)
        sem_results = self.semantic.retrieve(query, top_k=candidate_k)
        kw_results = self.keyword.retrieve(query, top_k=candidate_k)

        rrf_scores: Dict[str, float] = {}
        doc_map: Dict[str, Dict[str, Any]] = {}

        # Process semantic ranks
        for rank, doc in enumerate(sem_results):
            text_key = doc.get("text", "")
            doc_map[text_key] = doc
            rrf_scores[text_key] = rrf_scores.get(text_key, 0.0) + semantic_weight * (
                1.0 / (self.rrf_k + rank + 1)
            )

        # Process keyword ranks
        for rank, doc in enumerate(kw_results):
            text_key = doc.get("text", "")
            doc_map[text_key] = doc
            rrf_scores[text_key] = rrf_scores.get(text_key, 0.0) + keyword_weight * (
                1.0 / (self.rrf_k + rank + 1)
            )

        # Sort by fused score
        sorted_keys = sorted(rrf_scores.keys(), key=lambda k: rrf_scores[k], reverse=True)

        results: List[Dict[str, Any]] = []
        for k in sorted_keys[:top_k]:
            item = dict(doc_map[k])
            item["score"] = rrf_scores[k]
            item["retrieval_method"] = "hybrid_rrf"
            results.append(item)

        return results

    def clear(self) -> None:
        self.semantic.clear()
        self.keyword.clear()


# Default singleton instance
HYBRID_RETRIEVER = HybridRetriever()


def index_hybrid_documents(documents: List[Document]) -> None:
    HYBRID_RETRIEVER.index(documents)


def retrieve_hybrid(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    return HYBRID_RETRIEVER.retrieve(query, top_k=top_k)
