"""
Month-03 Day-05: Cross-Encoder Reranker & Context Compression
Implements:
1. Multi-stage retrieval reranking: Bi-encoder candidate generation -> Cross-encoder re-scoring.
2. Token-level cross-interaction scoring (simulating cross-attention interaction).
3. Dynamic Context Compression: Prunes low-scoring sentences to respect LLM context token budgets.
"""

from __future__ import annotations
import re
import sys
from typing import List, Dict, Any, Tuple
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CrossEncoderReranker:
    """
    Simulates a high-accuracy Cross-Encoder model.
    In cross-encoders, the query and document are passed jointly through attention:
    [CLS] Query [SEP] Document [SEP]
    Capturing full cross-attention term interactions and syntactic relationships.
    """

    def __init__(self, length_penalty: float = 0.05):
        self.length_penalty = length_penalty
        self.stopwords = {"the", "a", "an", "is", "are", "of", "and", "in", "to", "for", "why", "more", "than", "this", "that"}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def score_pair(self, query: str, document: str) -> float:
        """
        Calculates joint interaction score between query and document.
        Considers:
        1. Exact lexical alignment.
        2. Proximity and bigram co-occurrence.
        3. Length normalization.
        """
        q_tokens = [t for t in self._tokenize(query) if t not in self.stopwords]
        d_tokens = self._tokenize(document)

        if not q_tokens or not d_tokens:
            return 0.0

        d_counts = Counter(d_tokens)
        match_score = sum(d_counts.get(t, 0) for t in q_tokens)

        # Bigram co-occurrence check
        q_bigrams = {f"{q_tokens[i]}_{q_tokens[i+1]}" for i in range(len(q_tokens) - 1)}
        d_bigrams = Counter(f"{d_tokens[i]}_{d_tokens[i+1]}" for i in range(len(d_tokens) - 1))
        bigram_score = sum(d_bigrams.get(bg, 0) * 2.0 for bg in q_bigrams)

        total_score = (match_score * 1.5 + bigram_score * 3.0) / (1.0 + self.length_penalty * len(d_tokens))
        return round(float(total_score), 4)

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
        """Reranks candidate documents based on full cross-interaction."""
        scored = []
        for doc in candidates:
            score = self.score_pair(query, doc["text"])
            item = dict(doc)
            item["rerank_score"] = score
            scored.append(item)

        scored.sort(key=lambda x: x["rerank_score"], reverse=True)
        return scored[:top_k]


class ContextCompressor:
    """
    Compresses long passages by filtering out low-scoring sentences
    before stuffing context into an LLM prompt.
    """

    def __init__(self, reranker: CrossEncoderReranker, max_sentences_per_doc: int = 2):
        self.reranker = reranker
        self.max_sentences_per_doc = max_sentences_per_doc

    def compress_document(self, query: str, text: str) -> str:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?]) +", text) if s.strip()]
        if len(sentences) <= self.max_sentences_per_doc:
            return text

        scored = [(s, self.reranker.score_pair(query, s)) for s in sentences]
        scored.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s for s, _ in scored[: self.max_sentences_per_doc]]

        # Preserve original narrative ordering
        ordered = [s for s in sentences if s in top_sentences]
        return " ".join(ordered)


def run_demo():
    print("=" * 65)
    print("🚀 Day 05: Cross-Encoder Reranker & Context Compression")
    print("=" * 65)

    candidates = [
        {"id": "doc1", "text": "Deep neural networks require substantial GPU memory for inference."},
        {"id": "doc2", "text": "Cross-encoders evaluate query and document jointly, providing superior ranking accuracy over bi-encoders."},
        {"id": "doc3", "text": "Bi-encoders are fast because documents are indexed ahead of time independently of the query."},
    ]

    query = "Why are cross-encoders more accurate than bi-encoders for reranking?"

    reranker = CrossEncoderReranker()
    reranked = reranker.rerank(query, candidates, top_k=2)

    for i, doc in enumerate(reranked, 1):
        print(f"[{i}] Score: {doc['rerank_score']} | ID: {doc['id']}")
        print(f"    Text: {doc['text']}\n")

    assert reranked[0]["id"] == "doc2", "Doc 2 must be the top reranked document!"

    # Test Context Compression
    compressor = ContextCompressor(reranker, max_sentences_per_doc=2)
    long_doc = (
        "The weather in Seattle is rainy in November. "
        "Cross-encoders process query and text together through self-attention layers. "
        "Bananas are rich in potassium and healthy nutrients. "
        "This cross-encoder reranking mechanism delivers higher accuracy than bi-encoders."
    )
    compressed = compressor.compress_document(query, long_doc)
    print("Compressed Context:")
    print("   ", compressed)
    assert "Seattle" not in compressed and "Bananas" not in compressed

    print("\n✅ Day 05 Cross-Encoder & Compression Verification Successful!")


if __name__ == "__main__":
    run_demo()
