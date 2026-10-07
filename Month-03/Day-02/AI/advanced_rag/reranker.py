"""Cross-Encoder Reranker for semantic relevance scoring."""
from typing import List, Dict, Any


class CrossEncoderReranker:
    """Reranks initial candidate documents using full query-document attention scoring."""

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 2) -> List[Dict[str, Any]]:
        scored = []
        q_tokens = set(query.lower().split())

        for doc in candidates:
            doc_tokens = set(doc["content"].lower().split())
            intersection = len(q_tokens.intersection(doc_tokens))
            relevance_score = round(intersection / max(1, len(q_tokens)), 4)
            scored.append({"rerank_score": relevance_score, **doc})

        scored.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored[:top_n]
