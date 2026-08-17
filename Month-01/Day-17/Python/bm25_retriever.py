"""BM25 (Best Matching 25) Sparse Keyword Retrieval Implementation."""

import math
import re
from collections import Counter
from typing import Dict, List, Tuple


def tokenize(text: str) -> List[str]:
    """Tokenize and normalize text."""
    return re.findall(r"\b\w+\b", text.lower())


class BM25:
    """Okapi BM25 ranking algorithm."""

    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_tokens = [tokenize(doc) for doc in corpus]
        self.doc_lengths = [len(tokens) for tokens in self.doc_tokens]
        self.n_docs = len(corpus)
        self.avg_doc_len = sum(self.doc_lengths) / self.n_docs if self.n_docs > 0 else 0.0

        # Calculate Document Frequency (DF) and Inverse Document Frequency (IDF)
        self.df: Counter[str] = Counter()
        for tokens in self.doc_tokens:
            for term in set(tokens):
                self.df[term] += 1

        self.idf: Dict[str, float] = {}
        for term, freq in self.df.items():
            self.idf[term] = math.log((self.n_docs - freq + 0.5) / (freq + 0.5) + 1.0)

    def score_document(self, query_tokens: List[str], doc_idx: int) -> float:
        """Compute BM25 score for a document against query tokens."""
        term_freqs = Counter(self.doc_tokens[doc_idx])
        doc_len = self.doc_lengths[doc_idx]
        score = 0.0

        for term in query_tokens:
            if term in term_freqs:
                tf = term_freqs[term]
                idf = self.idf.get(term, 0.0)
                denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / (self.avg_doc_len or 1.0)))
                score += idf * (tf * (self.k1 + 1.0)) / denom

        return score

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Search the corpus and return top_k documents sorted by score."""
        q_tokens = tokenize(query)
        scored: List[Tuple[str, float]] = []

        for idx, doc in enumerate(self.corpus):
            score = self.score_document(q_tokens, idx)
            scored.append((doc, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [(doc, round(score, 4)) for doc, score in scored[:top_k] if score > 0]


if __name__ == "__main__":
    docs = [
        "Deep learning models require large datasets and GPUs for training.",
        "Retrieval-Augmented Generation (RAG) combines search retrieval with generative LLMs.",
        "BM25 is a ranking function used by search engines to estimate relevance of documents.",
        "Transformers utilize self-attention mechanisms to process tokens in parallel.",
    ]

    bm25 = BM25(corpus=docs)
    query = "How does BM25 rank search engine documents?"
    results = bm25.search(query, top_k=2)

    print("Query:", query)
    print("Top Results:")
    for rank, (doc, score) in enumerate(results, 1):
        print(f"{rank}. [Score: {score}] {doc}")
