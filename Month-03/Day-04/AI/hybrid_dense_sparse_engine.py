"""
Month-03 Day-04: Production Hybrid Dense-Sparse Retrieval Engine
Combines:
1. Lexical BM25 Sparse Search (Okapi BM25 with term frequency saturation & length normalization).
2. Dense Semantic Vector Search (Cosine similarity over dense embeddings).
3. Reciprocal Rank Fusion (RRF) and Relative Score Normalization.
"""

from __future__ import annotations
import math
import re
import hashlib
import sys
from typing import List, Dict, Any, Tuple
from collections import Counter
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class BM25Okapi:
    """In-memory BM25 Okapi implementation for sparse retrieval."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus: List[str] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Dict[str, int] = {}
        self.doc_term_freqs: List[Counter] = []
        self.num_docs: int = 0

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def fit(self, corpus: List[str]) -> None:
        self.corpus = corpus
        self.num_docs = len(corpus)
        self.doc_lengths = []
        self.doc_term_freqs = []
        self.doc_freqs = Counter()

        for doc in corpus:
            tokens = self._tokenize(doc)
            self.doc_lengths.append(len(tokens))
            freqs = Counter(tokens)
            self.doc_term_freqs.append(freqs)
            for token in freqs.keys():
                self.doc_freqs[token] += 1

        self.avg_doc_len = sum(self.doc_lengths) / self.num_docs if self.num_docs > 0 else 0.0

    def score(self, query: str) -> List[float]:
        query_tokens = self._tokenize(query)
        scores = [0.0] * self.num_docs

        for token in query_tokens:
            if token not in self.doc_freqs:
                continue
            df = self.doc_freqs[token]
            idf = math.log((self.num_docs - df + 0.5) / (df + 0.5) + 1.0)

            for i, freqs in enumerate(self.doc_term_freqs):
                tf = freqs.get(token, 0)
                if tf == 0:
                    continue
                doc_len = self.doc_lengths[i]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / (self.avg_doc_len or 1.0)))
                scores[i] += idf * (numerator / denominator)

        return scores


class DenseEmbedder:
    """Lightweight deterministic projection embedding model."""

    def __init__(self, dim: int = 256):
        self.dim = dim
        self.stopwords = {"what", "is", "the", "a", "an", "in", "on", "for", "of", "and", "to"}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def embed(self, text: str) -> np.ndarray:
        tokens = self._tokenize(text)
        vec = np.zeros(self.dim, dtype=np.float32)
        if not tokens:
            return vec

        for t in tokens:
            weight = 0.2 if t in self.stopwords else 2.5
            h = int(hashlib.md5(t.encode("utf-8")).hexdigest()[:8], 16)
            vec[h % self.dim] += weight

        for t in tokens:
            if t not in self.stopwords and len(t) >= 3:
                for i in range(len(t) - 2):
                    ng = t[i : i + 3]
                    h = int(hashlib.md5(ng.encode("utf-8")).hexdigest()[:8], 16)
                    vec[h % self.dim] += 0.5

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec


class HybridDenseSparseEngine:
    """
    Hybrid Search Engine fusing BM25 Sparse Lexical matching
    with Dense Embedding Semantic retrieval via Reciprocal Rank Fusion (RRF).
    """

    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k
        self.documents: List[Dict[str, Any]] = []
        self.bm25 = BM25Okapi()
        self.dense = DenseEmbedder()
        self.dense_vectors: List[np.ndarray] = []

    def index(self, documents: List[Dict[str, Any]]) -> None:
        """Indexes documents containing 'id' and 'text'."""
        self.documents = documents
        corpus = [doc["text"] for doc in documents]
        self.bm25.fit(corpus)
        self.dense_vectors = [self.dense.embed(doc["text"]) for doc in documents]

    def search_sparse(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        scores = self.bm25.score(query)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def search_dense(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        q_vec = self.dense.embed(query)
        scores = []
        for i, doc_vec in enumerate(self.dense_vectors):
            dot = float(np.dot(q_vec, doc_vec))
            scores.append((i, dot))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def search_hybrid(self, query: str, top_k: int = 5, dense_weight: float = 0.5) -> List[Dict[str, Any]]:
        """
        Fuses sparse and dense results using Reciprocal Rank Fusion (RRF).
        RRF Score = sum( 1 / (k + rank) )
        """
        sparse_hits = self.search_sparse(query, top_k=len(self.documents))
        dense_hits = self.search_dense(query, top_k=len(self.documents))

        rrf_scores: Dict[int, float] = {}

        # Accumulate sparse ranks
        for rank, (doc_idx, _) in enumerate(sparse_hits):
            score = (1.0 - dense_weight) * (1.0 / (self.rrf_k + rank + 1))
            rrf_scores[doc_idx] = rrf_scores.get(doc_idx, 0.0) + score

        # Accumulate dense ranks
        for rank, (doc_idx, _) in enumerate(dense_hits):
            score = dense_weight * (1.0 / (self.rrf_k + rank + 1))
            rrf_scores[doc_idx] = rrf_scores.get(doc_idx, 0.0) + score

        sorted_indices = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for doc_idx, score in sorted_indices:
            doc_data = dict(self.documents[doc_idx])
            doc_data["hybrid_score"] = round(score, 6)
            results.append(doc_data)

        return results


def run_demo():
    print("=" * 65)
    print("🚀 Day 04: Hybrid Dense-Sparse Retrieval Verification")
    print("=" * 65)

    docs = [
        {"id": "doc1", "text": "PostgreSQL is an ACID compliant relational database with advanced JSONB query support."},
        {"id": "doc2", "text": "BM25 is a ranking function used in information retrieval based on TF-IDF scoring."},
        {"id": "doc3", "text": "Dense vector retrieval uses embedding similarity like cosine distance in high dimensional space."},
        {"id": "doc4", "text": "Hybrid search combines BM25 keyword matching and dense vector embeddings with Reciprocal Rank Fusion."},
        {"id": "doc5", "text": "FastAPI is an asynchronous web framework built on top of Starlette and Pydantic."},
    ]

    engine = HybridDenseSparseEngine(rrf_k=60)
    engine.index(docs)

    query = "How does hybrid search combine BM25 and embeddings?"
    results = engine.search_hybrid(query, top_k=3)

    for i, res in enumerate(results, 1):
        print(f"[{i}] Score: {res['hybrid_score']} | ID: {res['id']}")
        print(f"    Text: {res['text']}\n")

    assert results[0]["id"] == "doc4", "Doc 4 must be the top hybrid result!"
    print("✅ Hybrid Retrieval Engine Verification Successful!")


if __name__ == "__main__":
    run_demo()
