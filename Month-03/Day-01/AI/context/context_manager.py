"""Production Context Manager uniting System instructions, Long-term Memories, and Sliding Windows."""
import sys
import os
from typing import List, Dict, Any, Optional

# Ensure Day-01 root is on python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.token_budget import TokenBudgetManager
from memory.conversation_memory import ConversationMemory
from memory.summarizer import ConversationSummarizer
from memory.memory_store import MemoryStore
from memory.memory_retrieval import MemoryRetrieval


class ContextManager:
    """Orchestrates comprehensive context assembly within strict token ceilings."""

    def __init__(self, system_prompt: str, user_id: str):
        self.system_prompt = system_prompt
        self.user_id = user_id
        self.budget_manager = TokenBudgetManager()
        self.memory = ConversationMemory(max_tokens=self.budget_manager.history_budget)
        self.summarizer = ConversationSummarizer()
        self.store = MemoryStore()
        self.retrieval = MemoryRetrieval(self.store)

    def assemble_context(self, current_user_query: str) -> List[Dict[str, str]]:
        """Assembles final prompt messages array respecting all token budgets."""
        # 1. Retrieve long-term memories
        relevant_memories = self.retrieval.retrieve_relevant_facts(self.user_id, current_user_query)
        memory_str = "\n".join([f"- {m}" for m in relevant_memories]) if relevant_memories else "No prior history."

        # 2. Build augmented system prompt
        full_system = f"{self.system_prompt}\n\n[USER RELEVANT MEMORY]:\n{memory_str}"

        # 3. Assemble messages
        messages = [{"role": "system", "content": full_system}]
        for turn in self.memory.get_history():
            messages.append(turn)
        messages.append({"role": "user", "content": current_user_query})

        return messages


if __name__ == "__main__":
    cm = ContextManager(
        system_prompt="You are an enterprise AI financial advisor.",
        user_id="user_449"
    )
    # Add long-term facts
    cm.store.add_episodic_memory("user_449", "User prefers conservative low-risk index ETF investments.")
    cm.store.add_episodic_memory("user_449", "User planning to buy a house in 2027.")

    # Record past turns
    cm.memory.add_user_message("What is my current investment preference?")
    cm.memory.add_assistant_message("You prefer conservative low-risk index ETF allocations.")

    assembled = cm.assemble_context("Should I invest in high-risk crypto today?")
    print("=== ASSEMBLED CONTEXT MESSAGES ===")
    for idx, msg in enumerate(assembled, 1):
        print(f"[{idx}] {msg['role'].upper()}:\n{msg['content']}\n")
