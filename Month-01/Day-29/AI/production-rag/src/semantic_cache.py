import math
import re
from typing import Dict, List, Optional, Tuple
from collections import Counter

class SemanticCache:
    """
    In-memory semantic cache using embedding/token cosine similarity.
    Bypasses costly retrieval and LLM generation when query similarity >= threshold.
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        # Stores list of entries: {"query": str, "vector": Counter, "response": str, "metadata": dict}
        self._entries: List[Dict] = []

    @staticmethod
    def _text_to_vector(text: str) -> Counter:
        tokens = re.findall(r"\b\w+\b", text.lower())
        return Counter(tokens)

    @staticmethod
    def _cosine_similarity(vec_a: Counter, vec_b: Counter) -> float:
        if not vec_a or not vec_b:
            return 0.0
        words = set(vec_a.keys()).union(set(vec_b.keys()))
        dot = sum(vec_a[w] * vec_b[w] for w in words)
        norm_a = math.sqrt(sum(c * c for c in vec_a.values()))
        norm_b = math.sqrt(sum(c * c for c in vec_b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def get(self, query: str) -> Optional[Tuple[str, float]]:
        q_vec = self._text_to_vector(query)
        best_match = None
        best_score = 0.0

        for entry in self._entries:
            sim = self._cosine_similarity(q_vec, entry["vector"])
            if sim > best_score:
                best_score = sim
                best_match = entry["response"]

        if best_score >= self.similarity_threshold and best_match:
            return best_match, round(best_score, 4)
        return None

    def set(self, query: str, response: str, metadata: Optional[Dict] = None):
        self._entries.append({
            "query": query,
            "vector": self._text_to_vector(query),
            "response": response,
            "metadata": metadata or {}
        })

    def clear(self):
        self._entries.clear()
