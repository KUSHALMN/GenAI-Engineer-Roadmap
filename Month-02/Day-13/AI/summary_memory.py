"""
Auto-Summarization Memory.
Hierarchically condenses older conversation turns into a progressive rolling summary
when message history exceeds a designated token budget.
"""

from typing import Callable, List, Optional
from conversation_memory import ChatMessage


class SummaryMemory:
    """Combines a rolling summary of older turns with the most recent raw dialogue turns."""

    def __init__(
        self,
        token_threshold: int = 150,
        keep_recent_k: int = 2,
        summarizer_func: Optional[Callable[[str, str], str]] = None,
    ):
        self.token_threshold = token_threshold
        self.keep_recent_k = keep_recent_k
        self.summarizer = summarizer_func or self._mock_summarizer
        self.current_summary = ""
        self.recent_messages: List[ChatMessage] = []

    def _mock_summarizer(self, current_summary: str, new_dialogue_text: str) -> str:
        """Simulates LLM progressive summarization."""
        combined = f"{current_summary}; {new_dialogue_text}".strip("; ")
        # Keep summary concise
        return f"Summary: User and Assistant discussed {combined[-80:]}"

    def add_turn(self, user_text: str, assistant_text: str) -> None:
        """Add a complete user-assistant interaction turn."""
        self.recent_messages.append(ChatMessage("user", user_text))
        self.recent_messages.append(ChatMessage("assistant", assistant_text))

        self._check_and_summarize()

    def _check_and_summarize(self) -> None:
        """If token budget exceeded, summarize oldest turns into rolling summary."""
        total_tokens = sum(m.token_count for m in self.recent_messages)
        if total_tokens > self.token_threshold and len(self.recent_messages) > self.keep_recent_k:
            # Separate messages to compress vs messages to keep
            num_to_summarize = len(self.recent_messages) - self.keep_recent_k
            to_compress = self.recent_messages[:num_to_summarize]
            self.recent_messages = self.recent_messages[num_to_summarize:]

            # Format dialogue to compress
            dialogue_str = " | ".join(f"{m.role}: {m.content}" for m in to_compress)
            self.current_summary = self.summarizer(self.current_summary, dialogue_str)

    def get_context_for_prompt(self) -> str:
        """Assemble summary + recent turns."""
        parts = []
        if self.current_summary:
            parts.append(f"Past Conversation Summary: {self.current_summary}")

        parts.append("Recent Dialogue:")
        for m in self.recent_messages:
            parts.append(f"{m.role.capitalize()}: {m.content}")

        return "\n".join(parts)


if __name__ == "__main__":
    mem = SummaryMemory(token_threshold=20, keep_recent_k=2)
    mem.add_turn("What is caching?", "Caching stores frequently accessed data in fast memory.")
    mem.add_turn("What is TTL?", "Time To Live determines when an item expires.")
    mem.add_turn("What is LRU?", "Least Recently Used evicts the oldest unaccessed item.")

    ctx = mem.get_context_for_prompt()
    print("Summarized Context:\n", ctx)
    assert "Past Conversation Summary:" in ctx
    assert len(mem.recent_messages) == 2
    print("SummaryMemory tests passed successfully!")
