"""
Cross-Encoder Reranker Pipeline
Bi-Encoder retrieves broad recall (Top-50) using fast independent embeddings.
Cross-Encoder performs full cross-attention between Query and Document pairs
for high-precision final re-ordering (Top-5).
"""

import math
from typing import List, Dict, Any, Tuple


class MockBiEncoder:
    """Simulates fast vector index retrieval (e.g. HNSW)"""
    def __init__(self, corpus: List[Dict[str, Any]]):
        self.corpus = corpus

    def retrieve(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        # Fast lexical + length heuristic
        q_words = set(query.lower().split())
        scored = []
        for doc in self.corpus:
            d_words = set(doc["text"].lower().split())
            overlap = len(q_words.intersection(d_words))
            scored.append((overlap, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]


class CrossEncoderReranker:
    """
    Simulates cross-attention joint interaction:
    Cross-attention models (e.g. bge-reranker-large, Cohere Rerank) process (Query, Document)
    in the same self-attention context, capturing term dependencies and exact semantics.
    """
    def score_pair(self, query: str, doc_text: str) -> float:
        q_words = query.lower().split()
        d_words = doc_text.lower().split()

        # Measure query coverage, exact sequence matching, and positional proximity
        coverage = sum(1.0 for w in q_words if w in d_words) / max(1, len(q_words))
        
        # Bigram match bonus (joint interaction)
        q_bigrams = [f"{q_words[i]} {q_words[i+1]}" for i in range(len(q_words) - 1)]
        bigram_matches = sum(1.0 for bg in q_bigrams if bg in doc_text.lower())
        bigram_bonus = (bigram_matches / max(1, len(q_bigrams))) * 0.5 if q_bigrams else 0.0

        # Penalize if document is overly generic
        length_penalty = 1.0 / (1.0 + 0.001 * abs(len(d_words) - 25))

        raw_score = (coverage * 0.7 + bigram_bonus * 0.3) * length_penalty
        # Sigmoid calibration to [0, 1]
        calibrated = 1.0 / (1.0 + math.exp(-6.0 * (raw_score - 0.4)))
        return round(calibrated, 4)

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        scored = []
        for doc in candidates:
            cross_score = self.score_pair(query, doc["text"])
            doc_copy = dict(doc)
            doc_copy["rerank_score"] = cross_score
            scored.append(doc_copy)

        scored.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored[:top_n]


if __name__ == "__main__":
    sample_corpus = [
        {"id": "doc_1", "text": "Python has decorators, generators, and dynamic typing for rapid web development."},
        {"id": "doc_2", "text": "Cross-encoder models pass the query and candidate chunk together into transformer attention layers."},
        {"id": "doc_3", "text": "Bi-encoders compute vector embeddings for documents independently and store them in vector indices."},
        {"id": "doc_4", "text": "Cross-encoders have high latency but superior precision compared to bi-encoder cosine similarity."},
        {"id": "doc_5", "text": "PostgreSQL relational databases support transaction ACID semantics and JSON storage."}
    ]

    bi_encoder = MockBiEncoder(sample_corpus)
    reranker = CrossEncoderReranker()

    query = "cross-encoder transformer attention layers precision"

    # Step 1: Candidate retrieval (Recall phase)
    initial_candidates = bi_encoder.retrieve(query, top_k=4)
    print("=== Step 1: Initial Bi-Encoder Retrieval (Recall Phase) ===")
    for c in initial_candidates:
        print(f"[{c['id']}] {c['text'][:65]}...")

    # Step 2: High-precision Reranking
    final_ranked = reranker.rerank(query, initial_candidates, top_n=3)
    print("\n=== Step 2: Post Cross-Encoder Reranking (Precision Phase) ===")
    for r in final_ranked:
        print(f"[{r['id']}] Score: {r['rerank_score']} -> {r['text'][:65]}...")
