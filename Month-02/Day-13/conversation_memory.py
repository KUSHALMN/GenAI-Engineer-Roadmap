"""
Conversation Memory Buffer.
Manages multi-turn dialogue history, role preservation, token estimation,
and window pruning.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ChatMessage:
    role: str  # "system", "user", "assistant"
    content: str
    token_count: int = 0

    def __post_init__(self):
        if not self.token_count:
            # Rule of thumb: ~4 characters per token
            self.token_count = max(1, len(self.content) // 4)


class ConversationMemory:
    """Sliding window chat memory."""

    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
        self.messages: List[ChatMessage] = []

    def add_message(self, role: str, content: str) -> None:
        """Add user or assistant message to dialogue."""
        msg = ChatMessage(role=role, content=content)
        self.messages.append(msg)
        self._prune()

    def _prune(self) -> None:
        """Prune oldest non-system messages if exceeding token limit."""
        while self.total_tokens() > self.max_tokens and len(self.messages) > 1:
            # Preserve system prompt if first
            if self.messages[0].role == "system":
                self.messages.pop(1)
            else:
                self.messages.pop(0)

    def total_tokens(self) -> int:
        return sum(m.token_count for m in self.messages)

    def get_messages(self) -> List[Dict[str, str]]:
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def clear(self) -> None:
        self.messages.clear()


if __name__ == "__main__":
    mem = ConversationMemory(max_tokens=60)
    mem.add_message("system", "You are a helpful AI assistant.")
    mem.add_message("user", "Hello there! This is a long query asking about database indexing techniques.")
    mem.add_message("assistant", "Database indexing speeds up queries by using B-Trees or Hash tables.")
    mem.add_message("user", "Can you explain B-Trees?")

    assert mem.messages[0].role == "system"
    assert len(mem.get_messages()) >= 2
    print("ConversationMemory tests passed successfully!")
