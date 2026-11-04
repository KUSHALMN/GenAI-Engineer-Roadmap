"""
Hybrid Search Engine - Dense + Sparse BM25 with Reciprocal Rank Fusion (RRF)
Demonstrates:
- Sparse BM25 ranking (TF-IDF probabilistic scoring)
- Dense vector similarity (cosine similarity with normalized dot product)
- Reciprocal Rank Fusion (RRF) score aggregation
- Convex linear score combination with MinMax normalization
"""

import math
from typing import List, Dict, Any, Tuple
from collections import Counter


class BM25Retriever:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs: List[Dict[str, Any]] = []
        self.doc_lens: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Counter = Counter()
        self.total_docs: int = 0

    def fit(self, docs: List[Dict[str, Any]]) -> "BM25Retriever":
        self.docs = docs
        self.total_docs = len(docs)
        self.doc_lens = []
        self.doc_freqs = Counter()

        for doc in docs:
            words = doc["text"].lower().split()
            self.doc_lens.append(len(words))
            unique_words = set(words)
            for w in unique_words:
                self.doc_freqs[w] += 1

        self.avg_doc_len = sum(self.doc_lens) / max(1, self.total_docs)
        return self

    def score(self, query: str) -> List[Tuple[int, float]]:
        query_terms = query.lower().split()
        scores = []

        for idx, doc in enumerate(self.docs):
            words = doc["text"].lower().split()
            tf_counter = Counter(words)
            doc_len = self.doc_lens[idx]
            doc_score = 0.0

            for q in query_terms:
                if q not in self.doc_freqs:
                    continue
                df = self.doc_freqs[q]
                # Standard Robertson-Spärck Jones IDF
                idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1.0)
                tf = tf_counter[q]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / max(1e-6, self.avg_doc_len)))
                doc_score += idf * (numerator / denominator)

            scores.append((idx, doc_score))

        return sorted(scores, key=lambda x: x[1], reverse=True)


class DenseRetriever:
    """Mock dense semantic retriever using word-vector embeddings"""
    def __init__(self):
        self.docs: List[Dict[str, Any]] = []
        self.vectors: List[List[float]] = []

    def _embed(self, text: str) -> List[float]:
        # Deterministic 16-dimensional hash embedding for testing
        vec = [0.0] * 16
        for i, word in enumerate(text.lower().split()):
            h = hash(word) % 16
            vec[h] += 1.0 / (i + 1)
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def fit(self, docs: List[Dict[str, Any]]) -> "DenseRetriever":
        self.docs = docs
        self.vectors = [self._embed(d["text"]) for d in docs]
        return self

    def score(self, query: str) -> List[Tuple[int, float]]:
        q_vec = self._embed(query)
        scores = []
        for idx, d_vec in enumerate(self.vectors):
            dot_product = sum(a * b for a, b in zip(q_vec, d_vec))
            scores.append((idx, dot_product))
        return sorted(scores, key=lambda x: x[1], reverse=True)


class HybridSearchEngine:
    def __init__(self, docs: List[Dict[str, Any]]):
        self.docs = docs
        self.bm25 = BM25Retriever().fit(docs)
        self.dense = DenseRetriever().fit(docs)

    def search_rrf(self, query: str, top_k: int = 5, rrf_k: int = 60) -> List[Dict[str, Any]]:
        """Reciprocal Rank Fusion aggregation: RRF_score = sum(1 / (k + rank_i))"""
        bm25_ranked = self.bm25.score(query)
        dense_ranked = self.dense.score(query)

        rrf_scores: Dict[int, float] = {i: 0.0 for i in range(len(self.docs))}

        for rank, (doc_idx, _) in enumerate(bm25_ranked, start=1):
            rrf_scores[doc_idx] += 1.0 / (rrf_k + rank)

        for rank, (doc_idx, _) in enumerate(dense_ranked, start=1):
            rrf_scores[doc_idx] += 1.0 / (rrf_k + rank)

        sorted_indices = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in sorted_indices[:top_k]:
            results.append({
                "id": self.docs[idx]["id"],
                "text": self.docs[idx]["text"],
                "rrf_score": round(score, 5),
                "metadata": self.docs[idx].get("metadata", {})
            })
        return results

    def search_weighted(self, query: str, dense_weight: float = 0.6, top_k: int = 5) -> List[Dict[str, Any]]:
        """Normalized linear combination: alpha * dense + (1 - alpha) * bm25"""
        bm25_scores = dict(self.bm25.score(query))
        dense_scores = dict(self.dense.score(query))

        # Min-max normalization for BM25
        b_vals = list(bm25_scores.values())
        b_min, b_max = min(b_vals), max(b_vals)
        b_range = b_max - b_min if b_max > b_min else 1.0

        d_vals = list(dense_scores.values())
        d_min, d_max = min(d_vals), max(d_vals)
        d_range = d_max - d_min if d_max > d_min else 1.0

        combined = []
        for idx in range(len(self.docs)):
            norm_b = (bm25_scores[idx] - b_min) / b_range
            norm_d = (dense_scores[idx] - d_min) / d_range
            final_score = (dense_weight * norm_d) + ((1.0 - dense_weight) * norm_b)
            combined.append((idx, final_score))

        combined.sort(key=lambda x: x[1], reverse=True)
        return [
            {
                "id": self.docs[idx]["id"],
                "text": self.docs[idx]["text"],
                "combined_score": round(sc, 4),
            }
            for idx, sc in combined[:top_k]
        ]


if __name__ == "__main__":
    sample_corpus = [
        {"id": "doc1", "text": "PostgreSQL relational database with pgvector for ACID transactions and vector storage."},
        {"id": "doc2", "text": "Elasticsearch distributed inverted index for full-text lexical search and BM25 relevance."},
        {"id": "doc3", "text": "Hybrid search combines dense embeddings and BM25 sparse keyword indices using RRF fusion."},
        {"id": "doc4", "text": "Convolutional neural network for computer vision and image classification tasks."},
        {"id": "doc5", "text": "Dense retrieval using transformer bi-encoder embeddings and approximate nearest neighbors."}
    ]

    engine = HybridSearchEngine(sample_corpus)
    query = "hybrid search BM25 vector retrieval"
    rrf_hits = engine.search_rrf(query, top_k=3)
    weighted_hits = engine.search_weighted(query, dense_weight=0.5, top_k=3)

    print("=== RRF Results ===")
    for h in rrf_hits:
        print(f"[{h['id']}] score={h['rrf_score']} -> {h['text'][:60]}...")

    print("\n=== Weighted Combined Results ===")
    for h in weighted_hits:
        print(f"[{h['id']}] score={h['combined_score']} -> {h['text'][:60]}...")
