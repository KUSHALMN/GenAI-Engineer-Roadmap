"""BM25 (Best Matching 25) Sparse Lexical Search Algorithm."""
import math
from typing import List, Dict, Any


class BM25Retriever:
    """Implements Okapi BM25 ranking algorithm."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: List[Dict[str, Any]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len = 0.0
        self.doc_freqs: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def fit(self, documents: List[Dict[str, Any]]):
        self.documents = documents
        total_len = 0
        self.doc_lengths = []
        self.doc_freqs.clear()

        for doc in documents:
            tokens = set(doc["content"].lower().split())
            doc_len = len(doc["content"].split())
            self.doc_lengths.append(doc_len)
            total_len += doc_len

            for token in tokens:
                self.doc_freqs[token] = self.doc_freqs.get(token, 0) + 1

        n_docs = len(documents)
        self.avg_doc_len = total_len / max(1, n_docs)

        # Compute Robertson-Spärck Jones IDF
        for token, freq in self.doc_freqs.items():
            self.idf[token] = math.log(1.0 + (n_docs - freq + 0.5) / (freq + 0.5))

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        q_tokens = query.lower().split()
        scores = []

        for idx, doc in enumerate(self.documents):
            score = 0.0
            doc_words = doc["content"].lower().split()
            doc_len = self.doc_lengths[idx]

            for token in q_tokens:
                if token not in self.idf:
                    continue
                tf = doc_words.count(token)
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                score += self.idf[token] * (numerator / max(1e-5, denominator))

            scores.append((score, doc))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [{"score": round(s, 4), **doc} for s, doc in scores[:top_k]]
