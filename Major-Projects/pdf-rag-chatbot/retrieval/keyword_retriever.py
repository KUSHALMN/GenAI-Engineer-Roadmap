from __future__ import annotations

import math
from collections import Counter
from typing import Any, Dict, List
from app.embedding import _tokenize
from app.loader import Document


class KeywordRetriever:
    """Retrieves top-k documents using BM25 keyword matching."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: List[Document] = []
        self.doc_tokens: List[List[str]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.idf: Dict[str, float] = {}

    def index(self, documents: List[Document]) -> None:
        """Build BM25 index across documents."""
        self.documents = list(documents)
        self.doc_tokens = [_tokenize(doc.text) for doc in self.documents]
        self.doc_lengths = [len(tokens) for tokens in self.doc_tokens]
        n_docs = len(self.documents)
        self.avg_doc_len = sum(self.doc_lengths) / n_docs if n_docs > 0 else 0.0

        # Calculate inverse document frequency
        df: Counter[str] = Counter()
        for tokens in self.doc_tokens:
            for term in set(tokens):
                df[term] += 1

        self.idf = {}
        for term, freq in df.items():
            # BM25 standard IDF with smoothing
            self.idf[term] = math.log((n_docs - freq + 0.5) / (freq + 0.5) + 1.0)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve top-k documents scoring by BM25."""
        if not self.documents or not query.strip():
            return []

        query_tokens = _tokenize(query)
        scores: List[tuple[float, Dict[str, Any]]] = []

        for idx, (doc, tokens, doc_len) in enumerate(
            zip(self.documents, self.doc_tokens, self.doc_lengths)
        ):
            term_counts = Counter(tokens)
            score = 0.0
            for q_term in query_tokens:
                if q_term in term_counts:
                    tf = term_counts[q_term]
                    idf_val = self.idf.get(q_term, 0.0)
                    denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / (self.avg_doc_len or 1.0)))
                    score += idf_val * (tf * (self.k1 + 1)) / denom

            if score > 0:
                meta = dict(doc.metadata)
                meta["text"] = doc.text
                meta["score"] = score
                scores.append((score, meta))

        scores.sort(key=lambda item: item[0], reverse=True)
        return [doc for score, doc in scores[:top_k]]

    def clear(self) -> None:
        """Clear the indexed keyword documents."""
        self.documents.clear()
        self.doc_tokens.clear()
        self.doc_lengths.clear()
        self.idf.clear()


# Default singleton instance
KEYWORD_RETRIEVER = KeywordRetriever()


def index_keyword_documents(documents: List[Document]) -> None:
    KEYWORD_RETRIEVER.index(documents)


def retrieve_keyword(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    return KEYWORD_RETRIEVER.retrieve(query, top_k=top_k)
