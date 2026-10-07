"""Retrieval of relevant past memory facts using semantic overlap."""
from typing import List, Dict, Any
from .memory_store import MemoryStore


class MemoryRetrieval:
    """Retrieves relevant past facts and long-term user context based on current query."""

    def __init__(self, store: MemoryStore):
        self.store = store

    def retrieve_relevant_facts(self, user_id: str, query: str, top_k: int = 2) -> List[str]:
        memories = self.store.get_all_memories(user_id)
        if not memories:
            return []

        q_tokens = set(query.lower().split())
        scored = []
        for m in memories:
            m_tokens = set(m["memory"].lower().split())
            overlap = len(q_tokens.intersection(m_tokens))
            scored.append((overlap, m["memory"]))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [mem for score, mem in scored[:top_k] if score > 0] or [m["memory"] for m in memories[:top_k]]
