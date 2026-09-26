"""
Hybrid Retriever with Reciprocal Rank Fusion (RRF).
Fuses Sparse (BM25 / Lexical frequency) and Dense (Cosine Vector Similarity) retrieval results.
RRF Formula: Score(d) = sum( 1 / (k + rank_i(d)) )
"""

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Document:
    doc_id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    dense_vector: Optional[List[float]] = None


class BM25Retriever:
    """Lightweight pure-python BM25 lexical retriever."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus: List[Document] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len = 0.0
        self.doc_freqs: Dict[str, int] = {}

    def index(self, documents: List[Document]) -> None:
        self.corpus = documents
        self.doc_lengths = [len(d.content.lower().split()) for d in documents]
        self.avg_doc_len = sum(self.doc_lengths) / max(len(self.doc_lengths), 1)

        self.doc_freqs.clear()
        for doc in documents:
            unique_words = set(doc.content.lower().split())
            for w in unique_words:
                self.doc_freqs[w] = self.doc_freqs.get(w, 0) + 1

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        q_tokens = query.lower().split()
        scores = []
        N = len(self.corpus)

        for idx, doc in enumerate(self.corpus):
            score = 0.0
            doc_tokens = doc.content.lower().split()
            doc_len = self.doc_lengths[idx]

            for term in q_tokens:
                if term not in self.doc_freqs:
                    continue
                tf = doc_tokens.count(term)
                df = self.doc_freqs[term]
                idf = math.log(1.0 + (N - df + 0.5) / (df + 0.5))
                term_score = idf * ((tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * (doc_len / max(self.avg_doc_len, 1)))))
                score += term_score

            scores.append((doc, round(score, 4)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class DenseRetriever:
    """Simulated dense vector retriever using cosine similarity."""

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        return dot / (norm1 * norm2) if norm1 and norm2 else 0.0

    def search(self, query_vec: List[float], documents: List[Document], top_k: int = 5) -> List[Tuple[Document, float]]:
        scores = []
        for doc in documents:
            if doc.dense_vector:
                sim = self.cosine_similarity(query_vec, doc.dense_vector)
                scores.append((doc, round(sim, 4)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class HybridRetriever:
    """Combines BM25 and Dense retrieval via Reciprocal Rank Fusion (RRF)."""

    def __init__(self, rrf_k: int = 60):
        self.bm25 = BM25Retriever()
        self.dense = DenseRetriever()
        self.rrf_k = rrf_k

    def reciprocal_rank_fusion(
        self,
        ranked_lists: List[List[Tuple[Document, float]]],
        top_k: int = 3,
    ) -> List[Tuple[Document, float]]:
        """
        Calculates RRF score: sum( 1 / (k + rank) ) across all ranking sources.
        """
        rrf_scores: Dict[str, float] = {}
        doc_lookup: Dict[str, Document] = {}

        for rank_list in ranked_lists:
            for rank, (doc, _) in enumerate(rank_list, start=1):
                doc_lookup[doc.doc_id] = doc
                rrf_scores[doc.doc_id] = rrf_scores.get(doc.doc_id, 0.0) + (1.0 / (self.rrf_k + rank))

        sorted_results = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [(doc_lookup[doc_id], round(score, 6)) for doc_id, score in sorted_results[:top_k]]


if __name__ == "__main__":
    docs = [
        Document("doc1", "Transformer models use attention mechanisms for sequences", dense_vector=[0.9, 0.1, 0.0]),
        Document("doc2", "BM25 is a ranking function used by search engines", dense_vector=[0.1, 0.8, 0.2]),
        Document("doc3", "Hybrid search combines sparse BM25 and dense vector embeddings", dense_vector=[0.7, 0.6, 0.3]),
    ]

    retriever = HybridRetriever()
    retriever.bm25.index(docs)

    bm25_res = retriever.bm25.search("hybrid vector search", top_k=3)
    dense_res = retriever.dense.search([0.7, 0.6, 0.3], docs, top_k=3)

    fused = retriever.reciprocal_rank_fusion([bm25_res, dense_res], top_k=2)
    print("Fused Results:", [(d[0].doc_id, d[1]) for d in fused])
    assert fused[0][0].doc_id == "doc3"  # doc3 appears top in both lists
    print("Hybrid retriever tests passed successfully!")
