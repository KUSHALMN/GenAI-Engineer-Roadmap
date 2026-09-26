"""
Dataset Deduplication Suite.
Implements:
1. Exact Deduplication via SHA-256 content hashing.
2. Fuzzy / Near-Duplicate Detection using Character N-gram Jaccard Similarity.
"""

import hashlib
import re
from typing import Any, Dict, List, Set, Tuple


class Deduplicator:

    @staticmethod
    def compute_hash(text: str) -> str:
        """Normalized SHA-256 content hash."""
        normalized = " ".join(text.lower().split())
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def get_ngrams(text: str, n: int = 3) -> Set[str]:
        """Extract word or character n-grams."""
        clean = re.sub(r"[^\w\s]", "", text.lower())
        words = clean.split()
        if len(words) < n:
            return set(words)
        return {" ".join(words[i:i+n]) for i in range(len(words) - n + 1)}

    @classmethod
    def jaccard_similarity(cls, set1: Set[str], set2: Set[str]) -> float:
        """Calculate Jaccard overlap coefficient."""
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    @classmethod
    def exact_deduplicate(cls, documents: List[Dict[str, Any]], text_key: str = "text") -> Tuple[List[Dict[str, Any]], int]:
        """Removes exact duplicates. Returns (deduped_docs, num_duplicates_removed)."""
        seen_hashes = set()
        deduped = []
        duplicates = 0

        for doc in documents:
            text = doc.get(text_key, "")
            h = cls.compute_hash(text)
            if h in seen_hashes:
                duplicates += 1
            else:
                seen_hashes.add(h)
                deduped.append(doc)

        return deduped, duplicates

    @classmethod
    def fuzzy_deduplicate(
        cls,
        documents: List[Dict[str, Any]],
        text_key: str = "text",
        threshold: float = 0.80,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Removes near-duplicate documents exceeding Jaccard threshold."""
        retained = []
        retained_ngrams: List[Set[str]] = []
        near_duplicates = 0

        for doc in documents:
            text = doc.get(text_key, "")
            ng = cls.get_ngrams(text, n=2)

            is_dup = False
            for existing_ng in retained_ngrams:
                sim = cls.jaccard_similarity(ng, existing_ng)
                if sim >= threshold:
                    is_dup = True
                    break

            if is_dup:
                near_duplicates += 1
            else:
                retained.append(doc)
                retained_ngrams.append(ng)

        return retained, near_duplicates


if __name__ == "__main__":
    docs = [
        {"id": 1, "text": "Deploying models to production requires rigorous latency tracking."},
        {"id": 2, "text": "Deploying models to production requires rigorous latency tracking."},  # exact dup
        {"id": 3, "text": "Deploying models into production requires rigorous latency tracking and monitoring."},  # near dup
        {"id": 4, "text": "Quantum computing uses qubits and superposition principles."},  # distinct
    ]

    # Exact
    exact_clean, exact_dups = Deduplicator.exact_deduplicate(docs)
    assert len(exact_clean) == 3
    assert exact_dups == 1

    # Fuzzy
    fuzzy_clean, fuzzy_dups = Deduplicator.fuzzy_deduplicate(exact_clean, threshold=0.40)
    assert len(fuzzy_clean) == 2
    assert fuzzy_dups == 1

    print("Deduplicator tests passed successfully!")
