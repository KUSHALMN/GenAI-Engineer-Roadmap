"""
Master Context Window Manager.
Assembles prompt context within a strict token budget:
System Instructions (Fixed) + Long-term Memory Facts + Rolling Dialogue Summary + Recent Messages.
"""

from typing import Any, Dict, List, Optional
from conversation_memory import ConversationMemory
from memory_retrieval import LongTermMemoryStore
from summary_memory import SummaryMemory


class ContextManager:
    """Orchestrates all memory tiers into a consolidated LLM prompt payload."""

    def __init__(
        self,
        max_total_tokens: int = 4000,
        system_instruction: str = "You are an expert AI software engineer.",
    ):
        self.max_tokens = max_total_tokens
        self.system_instruction = system_instruction
        self.long_term_store = LongTermMemoryStore()
        self.summary_memory = SummaryMemory(token_threshold=400, keep_recent_k=4)

    def assemble_prompt(self, user_query: str) -> List[Dict[str, str]]:
        """
        Builds the messages list for LLM API call:
        1. System message (Instructions + Retrieved Long-Term Facts)
        2. Summary message (if exists)
        3. Recent conversation messages
        4. Current user query
        """
        # 1. Retrieve relevant facts
        facts = self.long_term_store.retrieve(user_query, top_k=2)
        fact_str = ""
        if facts:
            fact_str = "\nRelevant Long-Term User Facts:\n" + "\n".join(f"- {f[0].fact}" for f in facts)

        full_system_content = f"{self.system_instruction}{fact_str}"

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": full_system_content}
        ]

        # 2. Add summary if available
        if self.summary_memory.current_summary:
            messages.append({
                "role": "system",
                "content": f"[Conversation History Summary: {self.summary_memory.current_summary}]"
            })

        # 3. Add recent dialogue
        for m in self.summary_memory.recent_messages:
            messages.append({"role": m.role, "content": m.content})

        # 4. Current turn
        messages.append({"role": "user", "content": user_query})

        return messages


if __name__ == "__main__":
    cm = ContextManager(max_total_tokens=2000)
    cm.long_term_store.write_fact("stack", "User prefers Python backend and Java for algorithms")
    cm.summary_memory.add_turn("What is RAG?", "Retrieval Augmented Generation combines vector search with LLMs.")

    prompt_payload = cm.assemble_prompt("Write an algorithm to sort numbers")
    print("Assembled Prompt Payload:", prompt_payload)
    assert len(prompt_payload) >= 3
    assert "Python backend and Java" in prompt_payload[0]["content"]
    print("ContextManager tests passed successfully!")
