"""
Day 11: Agent Memory Integration
Demonstrates a multi-tiered agent memory architecture:
1. Working Memory (ephemeral scratchpad for current subtask)
2. Episodic Memory (conversation history with compaction)
3. Semantic Long-Term Memory (vector-style associative fact retrieval)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import math

@dataclass
class MemoryRecord:
    id: str
    content: str
    category: str # "episodic", "semantic", "working"
    importance: float = 1.0

class MultiTierMemory:
    def __init__(self, working_token_limit: int = 1000):
        self.working_memory: List[str] = []
        self.episodic_history: List[Dict[str, str]] = []
        self.semantic_store: List[MemoryRecord] = []
        self.working_token_limit = working_token_limit

    def add_working_step(self, step_info: str):
        self.working_memory.append(step_info)

    def add_episodic(self, role: str, content: str):
        self.episodic_history.append({"role": role, "content": content})

    def store_semantic_fact(self, record_id: str, fact: str, importance: float = 1.0):
        self.semantic_store.append(MemoryRecord(id=record_id, content=fact, category="semantic", importance=importance))

    def recall_semantic(self, query: str, top_k: int = 2) -> List[MemoryRecord]:
        """Simple keyword/overlap similarity for memory recall."""
        q_words = set(query.lower().split())
        scored = []
        for rec in self.semantic_store:
            r_words = set(rec.content.lower().split())
            overlap = len(q_words.intersection(r_words))
            score = overlap * rec.importance
            if score > 0:
                scored.append((score, rec))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in scored[:top_k]]

    def assemble_prompt_context(self, user_query: str) -> str:
        semantic_recalled = self.recall_semantic(user_query)
        semantic_text = "\n".join(f"- {r.content}" for r in semantic_recalled)
        working_text = "\n".join(self.working_memory[-5:]) # Latest working steps
        
        return f"""[Relevant Semantic Memory]
{semantic_text if semantic_text else 'None'}

[Working Scratchpad]
{working_text if working_text else 'Empty'}
"""

if __name__ == "__main__":
    mem = MultiTierMemory()
    mem.store_semantic_fact("user_pref", "User prefers dark mode and concise Python code.", importance=1.5)
    mem.store_semantic_fact("user_role", "User is a staff AI infrastructure engineer.", importance=1.2)
    mem.store_semantic_fact("org_policy", "Deployments to prod require signed git tags.", importance=2.0)

    mem.add_working_step("Checked status of redis cluster.")
    mem.add_working_step("Identified 2 unindexed documents.")

    context = mem.assemble_prompt_context("How should I write the Python script?")
    print("Assembled Prompt Context:")
    print(context)
    assert "concise Python code" in context
    print("Day 11 AI Multi-Tier Memory passed all tests.")
