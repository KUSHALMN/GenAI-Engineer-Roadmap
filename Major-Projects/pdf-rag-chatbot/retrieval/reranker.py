from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List
import numpy as np
from app.embedding import _tokenize, cosine_similarity, embed_texts


class Reranker:
    """Reranks candidate retrieved passages based on cross-attention / multi-feature relevance scoring."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._cross_model = None
        self._try_load_cross_encoder()

    def _try_load_cross_encoder(self) -> None:
        try:
            from sentence_transformers import CrossEncoder

            self._cross_model = CrossEncoder(self.model_name)
        except Exception:
            self._cross_model = None

    def rerank(
        self, query: str, candidate_docs: List[Dict[str, Any]], top_k: int = 4
    ) -> List[Dict[str, Any]]:
        """Rerank candidate passages to prioritize high-precision matches."""
        if not candidate_docs:
            return []

        if self._cross_model is not None:
            pairs = [[query, doc.get("text", "")] for doc in candidate_docs]
            scores = self._cross_model.predict(pairs)
            scored_candidates = []
            for doc, score in zip(candidate_docs, scores):
                item = dict(doc)
                item["rerank_score"] = float(score)
                scored_candidates.append(item)
            scored_candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
            return scored_candidates[:top_k]

        # Robust multi-signal scoring fallback (Token Jaccard + Semantic Cosine + Exact Substring Match)
        query_tokens = set(_tokenize(query))
        query_emb = embed_texts([query])[0]
        doc_texts = [d.get("text", "") for d in candidate_docs]
        doc_embs = embed_texts(doc_texts)

        scored_candidates: List[Dict[str, Any]] = []

        for doc, doc_emb in zip(candidate_docs, doc_embs):
            text = doc.get("text", "")
            doc_tokens = set(_tokenize(text))

            # 1. Jaccard token overlap
            intersection = len(query_tokens.intersection(doc_tokens))
            union = len(query_tokens.union(doc_tokens))
            jaccard = intersection / union if union > 0 else 0.0

            # 2. Embedding Cosine Similarity
            sem_sim = cosine_similarity(query_emb, doc_emb)

            # 3. Exact query substring bonus
            substr_bonus = 0.2 if query.lower().strip() in text.lower() else 0.0

            # Combined multi-feature rerank score
            final_score = 0.5 * sem_sim + 0.3 * jaccard + substr_bonus

            item = dict(doc)
            item["rerank_score"] = round(final_score, 4)
            scored_candidates.append(item)

        scored_candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored_candidates[:top_k]


# Default singleton instance
RERANKER = Reranker()


def rerank(
    query: str, candidate_docs: List[Dict[str, Any]], top_k: int = 4
) -> List[Dict[str, Any]]:
    return RERANKER.rerank(query, candidate_docs, top_k=top_k)
