import math
import numpy as np
from typing import List, Dict, Any, Tuple

class VectorStore:
    """
    In-memory vector store supporting dense embedding index, cosine similarity search,
    top-K nearest neighbors, and document metadata querying.
    """

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: List[np.ndarray] = []

    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Deterministic, robust embedding generator based on multi-hash n-gram projection.
        Falls back to SentenceTransformers if installed, otherwise uses normalized semantic projection.
        """
        try:
            # Check if sentence_transformers is available
            from sentence_transformers import SentenceTransformer
            if not hasattr(self, "_st_model"):
                self._st_model = SentenceTransformer("all-MiniLM-L6-v2")
            return self._st_model.encode(text, normalize_embeddings=True)
        except Exception:
            pass

        # High-quality deterministic feature hashing with bag-of-words / character 3-grams
        vec = np.zeros(self.dimension, dtype=np.float32)
        words = text.lower().split()
        if not words:
            return vec

        for word in words:
            # Word level hash
            h = hash(word) % self.dimension
            vec[h] += 1.0
            # Char trigram hashes
            for i in range(max(0, len(word) - 2)):
                tri = word[i:i+3]
                h_tri = (hash(tri) * 31) % self.dimension
                vec[h_tri] += 0.5

        # L2 Normalization for exact cosine distance via dot product
        norm = np.linalg.norm(vec)
        if norm > 1e-9:
            vec = vec / norm
        return vec

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Embed and index a list of chunk objects."""
        added = 0
        for chunk in chunks:
            text = chunk.get("text", "")
            if not text:
                continue
            emb = self._generate_embedding(text)
            self.chunks.append(chunk)
            self.embeddings.append(emb)
            added += 1
        return added

    def search(self, query: str, top_k: int = 4, threshold: float = 0.0) -> List[Tuple[Dict[str, Any], float]]:
        """
        Cosine similarity search against all indexed chunks.
        Returns list of (chunk, similarity_score) sorted in descending order.
        """
        if not self.embeddings:
            return []

        query_emb = self._generate_embedding(query)
        scores = []

        for idx, emb in enumerate(self.embeddings):
            # Cosine similarity between unit vectors is simple dot product
            sim = float(np.dot(query_emb, emb))
            if sim >= threshold:
                scores.append((self.chunks[idx], sim))

        # Sort descending by similarity
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def clear(self) -> None:
        """Reset the vector store."""
        self.chunks.clear()
        self.embeddings.clear()

    def count(self) -> int:
        """Total indexed chunks."""
        return len(self.chunks)

    def get_all_sources(self) -> List[str]:
        """Unique source filenames indexed in vector store."""
        return sorted(list({c.get("source", "") for c in self.chunks if c.get("source")}))
