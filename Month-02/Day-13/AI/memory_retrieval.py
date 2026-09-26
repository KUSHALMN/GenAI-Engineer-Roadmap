"""
Long-Term Episodic Memory Retrieval & Conflict Resolution.
Implements:
1. Memory storage with key-value/semantic indexing and timestamping
2. Conflict resolution policy (LWW - Last Write Wins, or higher confidence score)
3. Decay & stale memory pruning
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class MemoryFact:
    key: str
    fact: str
    timestamp: float = field(default_factory=time.time)
    confidence: float = 1.0
    source: str = "user_input"


class LongTermMemoryStore:
    """
    Episodic memory store with conflict management and retrieval policies.
    """

    def __init__(self, stale_threshold_seconds: float = 86400.0 * 30):  # 30 days default
        self.facts: Dict[str, MemoryFact] = {}
        self.stale_threshold = stale_threshold_seconds

    def write_fact(
        self,
        key: str,
        fact: str,
        confidence: float = 1.0,
        source: str = "user_input",
    ) -> str:
        """
        Store or update a fact using Last-Write-Wins and Confidence policies.
        Resolves conflicts if key already exists.
        """
        clean_key = key.strip().lower()

        if clean_key in self.facts:
            existing = self.facts[clean_key]
            # Policy 1: If existing has significantly higher confidence, retain existing
            if existing.confidence > confidence + 0.3:
                return f"Conflict ignored: existing fact has higher confidence ({existing.confidence} vs {confidence})"

            # Policy 2: Otherwise overwrite with newer fact (Last Write Wins)
            self.facts[clean_key] = MemoryFact(
                key=clean_key,
                fact=fact,
                timestamp=time.time(),
                confidence=confidence,
                source=source,
            )
            return "Updated existing memory fact (Last Write Wins)"

        self.facts[clean_key] = MemoryFact(
            key=clean_key,
            fact=fact,
            timestamp=time.time(),
            confidence=confidence,
            source=source,
        )
        return "Stored new memory fact"

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[MemoryFact, float]]:
        """
        Retrieves relevant memory facts based on query term overlap score.
        Filters out expired/stale facts.
        """
        q_words = [w.strip(".,!?").lower() for w in query.split() if len(w) > 2]
        scored: List[Tuple[MemoryFact, float]] = []
        now = time.time()

        for key, mem in self.facts.items():
            # Check staleness
            if now - mem.timestamp > self.stale_threshold:
                continue

            fact_words = [w.strip(".,!?").lower() for w in mem.fact.split() if len(w) > 2]
            key_words = [w.strip(".,!?").lower() for w in key.replace("_", " ").split() if len(w) > 2]
            target_words = set(fact_words + key_words)

            matched = 0
            for qw in q_words:
                if any(qw in tw or tw in qw for tw in target_words):
                    matched += 1

            if matched > 0:
                score = (matched / max(len(q_words), 1)) * mem.confidence
                scored.append((mem, round(score, 3)))

        # Sort descending by score
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def clear(self) -> None:
        self.facts.clear()


if __name__ == "__main__":
    store = LongTermMemoryStore()

    # Fact 1: User preferences
    store.write_fact("user_language", "User prefers answers written in Python and Java", confidence=0.9)
    # Fact 2: Framework preference
    store.write_fact("preferred_framework", "User uses FastAPI for web services", confidence=0.8)

    # Retrieval
    matches = store.retrieve("What programming language does the user prefer?")
    print("Retrieved facts:", [(m[0].fact, m[1]) for m in matches])
    assert len(matches) > 0
    assert "Python and Java" in matches[0][0].fact

    # Conflict test: Overwrite framework
    store.write_fact("preferred_framework", "User switched from FastAPI to Next.js", confidence=0.95)
    updated = store.retrieve("preferred framework")
    assert "Next.js" in updated[0][0].fact

    print("Long-term memory retrieval tests passed successfully!")
