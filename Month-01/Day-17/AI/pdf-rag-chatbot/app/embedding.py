from __future__ import annotations

import math
import re
from typing import List, Sequence
import numpy as np


def _tokenize(text: str) -> List[str]:
    """Lowercase and extract alphanumeric word tokens."""
    return re.findall(r"\b\w+\b", text.lower())


def cosine_similarity(v1: Sequence[float], v2: Sequence[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a = np.array(v1, dtype=np.float32)
    b = np.array(v2, dtype=np.float32)
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


class EmbeddingModel:
    """Embedding model wrapper using SentenceTransformers if available, with deterministic fallback."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", dim: int = 384):
        self.model_name = model_name
        self.dim = dim
        self._st_model = None
        self._try_load_st()

    def _try_load_st(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer

            self._st_model = SentenceTransformer(self.model_name)
        except Exception:
            self._st_model = None

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate dense embedding vectors for a list of text strings."""
        if not texts:
            return []

        if self._st_model is not None:
            embeddings = self._st_model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()

        # Deterministic lightweight dense projection fallback with term weighting
        import hashlib

        stopwords = {"what", "is", "a", "the", "of", "in", "for", "with", "from", "to", "and", "an", "are", "this", "that"}
        embeddings: List[List[float]] = []
        for text in texts:
            tokens = _tokenize(text)
            vector = np.zeros(self.dim, dtype=np.float32)
            if not tokens:
                embeddings.append(vector.tolist())
                continue

            for t in tokens:
                weight = 0.2 if t in stopwords else 3.0
                h = int(hashlib.md5(t.encode("utf-8")).hexdigest()[:8], 16)
                vector[h % self.dim] += weight

            for t in tokens:
                if t not in stopwords and len(t) >= 3:
                    for i in range(len(t) - 2):
                        ng = t[i : i + 3]
                        h = int(hashlib.md5(ng.encode("utf-8")).hexdigest()[:8], 16)
                        vector[h % self.dim] += 0.5

            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm
            embeddings.append(vector.tolist())

        return embeddings

    def embed_query(self, query: str) -> List[float]:
        """Embed a single search query."""
        return self.embed_texts([query])[0]


# Singleton default embedder
embedder = EmbeddingModel()


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Helper functional embedding call."""
    return embedder.embed_texts(texts)
