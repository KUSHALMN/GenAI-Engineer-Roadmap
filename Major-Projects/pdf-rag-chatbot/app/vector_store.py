from __future__ import annotations

from typing import Any, Dict, List
import numpy as np
from app.embedding import cosine_similarity


class VectorStore:
    """In-memory Vector Store with cosine similarity indexing."""

    def __init__(self):
        self.vectors: List[List[float]] = []
        self.documents: List[Dict[str, Any]] = []

    def add(self, vector: List[float], metadata: Dict[str, Any]) -> None:
        """Add a single embedding vector and associated metadata."""
        self.vectors.append(vector)
        self.documents.append(metadata)

    def add_batch(
        self, vectors: List[List[float]], documents: List[Dict[str, Any]]
    ) -> None:
        """Add multiple vectors and metadata records."""
        for v, d in zip(vectors, documents):
            self.add(v, d)

    def search(
        self, query_vector: List[float], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search the store for the most similar documents given a query vector."""
        if not self.vectors:
            return []

        scores: List[tuple[float, Dict[str, Any]]] = []
        for vec, doc in zip(self.vectors, self.documents):
            score = cosine_similarity(query_vector, vec)
            scored_doc = dict(doc)
            scored_doc["score"] = score
            scores.append((score, scored_doc))

        scores.sort(key=lambda item: item[0], reverse=True)
        return [doc for score, doc in scores[:top_k]]

    def clear(self) -> None:
        """Clear all stored vectors and documents."""
        self.vectors.clear()
        self.documents.clear()

    def count(self) -> int:
        """Return the number of indexed records."""
        return len(self.documents)
