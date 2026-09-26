"""
Reranker Module for Advanced RAG.
Acts as a second-stage cross-encoder ranker that scores deep query-document interaction
to reorder top retrieved candidate chunks.
"""

import math
from typing import Any, Callable, Dict, List, Optional, Tuple
from hybrid_retriever import Document


class Reranker:
    """
    Reranks candidate documents.
    Supports heuristic lexical-semantic cross-scoring or neural cross-encoders.
    """

    def __init__(self, scoring_fn: Optional[Callable[[str, str], float]] = None):
        self.scoring_fn = scoring_fn or self._cross_attention_heuristic

    def _cross_attention_heuristic(self, query: str, doc_text: str) -> float:
        """
        Simulates cross-encoder deep interaction:
        Combines exact term matches, phrase alignment, and length normalization.
        """
        q_words = [w.lower().strip(".,!?") for w in query.split() if len(w) > 2]
        d_words = [w.lower().strip(".,!?") for w in doc_text.split() if len(w) > 2]

        if not q_words or not d_words:
            return 0.0

        # Term intersection
        term_matches = sum(1 for qw in q_words if qw in d_words)
        term_ratio = term_matches / len(q_words)

        # Bigram match
        q_bigrams = {" ".join(q_words[i:i+2]) for i in range(len(q_words) - 1)}
        d_text_lower = doc_text.lower()
        bigram_matches = sum(1 for bg in q_bigrams if bg in d_text_lower)
        bigram_ratio = bigram_matches / max(len(q_bigrams), 1)

        # Cross score
        score = 0.6 * term_ratio + 0.4 * bigram_ratio
        return round(score, 4)

    def rerank(self, query: str, candidates: List[Document], top_n: int = 3) -> List[Tuple[Document, float]]:
        """
        Takes candidate documents from initial retrieval and reranks them.
        """
        scored = []
        for doc in candidates:
            score = self.scoring_fn(query, doc.content)
            scored.append((doc, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_n]


if __name__ == "__main__":
    docs = [
        Document("docA", "Transformers were introduced in the paper Attention is All You Need."),
        Document("docB", "Cars use internal combustion engines or electric motors for propulsion."),
        Document("docC", "The attention mechanism allows transformers to process sequences effectively."),
    ]

    reranker = Reranker()
    ranked = reranker.rerank("What is the attention mechanism in transformers?", docs, top_n=2)
    print("Reranked:", [(d[0].doc_id, d[1]) for d in ranked])
    assert ranked[0][0].doc_id in ("docC", "docA")
    assert ranked[0][1] > 0.5
    print("Reranker tests passed successfully!")
