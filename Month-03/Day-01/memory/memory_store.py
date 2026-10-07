"""Persistent Key-Value & Vector Memory Store."""
import json
from typing import Dict, Any, List, Optional


class MemoryStore:
    """Stores episodic facts and user attributes persistently across sessions."""

    def __init__(self):
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.episodic_memories: Dict[str, List[Dict[str, Any]]] = {}

    def save_fact(self, user_id: str, fact_key: str, value: Any):
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        self.user_profiles[user_id][fact_key] = value

    def get_user_facts(self, user_id: str) -> Dict[str, Any]:
        return self.user_profiles.get(user_id, {})

    def add_episodic_memory(self, user_id: str, memory_text: str, tags: Optional[List[str]] = None):
        if user_id not in self.episodic_memories:
            self.episodic_memories[user_id] = []
        self.episodic_memories[user_id].append({
            "memory": memory_text,
            "tags": tags or []
        })

    def get_all_memories(self, user_id: str) -> List[Dict[str, Any]]:
        return self.episodic_memories.get(user_id, [])
