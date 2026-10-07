"""Cross-modal CLIP-style image & text embedding generator."""
import math
import hashlib
from typing import List, Dict, Any


class ImageEmbeddingGenerator:
    """Generates normalized vector representations for images and text in shared latent space."""

    def __init__(self, dim: int = 128):
        self.dim = dim

    def embed_text(self, text: str) -> List[float]:
        return self._hash_to_unit_vector(text)

    def embed_image(self, image_descriptor: str) -> List[float]:
        return self._hash_to_unit_vector(f"img_{image_descriptor}")

    def _hash_to_unit_vector(self, seed: str) -> List[float]:
        # Deterministic pseudo-embedding for testing cross-modal geometry
        h = hashlib.sha256(seed.encode("utf-8")).digest()
        vec = [(float(b) - 128.0) / 128.0 for b in h[:self.dim]]
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [round(x / norm, 4) for x in vec]

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        return round(dot, 4)
