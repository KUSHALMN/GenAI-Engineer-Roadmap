"""
Session Manager Module
Orchestrates multi-turn conversation sessions, thread routing,
cross-turn memory extraction, and conversational context compaction.
"""

import time
from typing import Dict, List, Optional
from schemas import MemoryEntry, ResearchReport
from memory.memory_store import MemoryStore, global_memory_store
from config import config


class SessionManager:
    """
    Manages active session threads and provides cross-turn episodic memory.
    """

    def __init__(self, memory_store: Optional[MemoryStore] = None):
        self.store = memory_store or global_memory_store
        self.session_memories: Dict[str, List[MemoryEntry]] = {}

    def get_session_memory(self, session_id: str) -> List[MemoryEntry]:
        """Returns the list of past memory entries for a given session."""
        return self.session_memories.get(session_id, [])

    def record_turn(self, session_id: str, query: str, report: ResearchReport):
        """Extracts key insights from a completed research report and saves to session memory."""
        if session_id not in self.session_memories:
            self.session_memories[session_id] = []

        turn_id = len(self.session_memories[session_id]) + 1
        
        # Extract salient metrics as key facts
        facts = []
        for k, v in report.key_metrics.items():
            facts.append(f"{k}: {v}")

        entry = MemoryEntry(
            turn_id=turn_id,
            query=query,
            summary=report.executive_summary[:280] + "...",
            key_facts=facts,
            timestamp=time.time()
        )

        self.session_memories[session_id].append(entry)

        # Enforce max history window
        if len(self.session_memories[session_id]) > config.max_history_turns:
            self.session_memories[session_id] = self.session_memories[session_id][-config.max_history_turns:]

    def format_memory_context(self, session_id: str) -> str:
        """Formats past session memory into a readable prompt context for the agent."""
        memories = self.get_session_memory(session_id)
        if not memories:
            return "No previous conversational memory for this session."

        lines = ["### Previous Conversational Context:"]
        for m in memories:
            lines.append(f"- [Turn {m.turn_id}] Query: '{m.query}'")
            lines.append(f"  Summary: {m.summary}")
            if m.key_facts:
                lines.append(f"  Verified Facts: {'; '.join(m.key_facts)}")
        return "\n".join(lines)


# Global Session Manager Instance
global_session_manager = SessionManager()
