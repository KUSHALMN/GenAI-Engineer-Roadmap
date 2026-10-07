"""Sliding Window and Buffer Conversation Memory."""
from typing import List, Dict, Any
from .token_budget import TokenBudgetManager


class ConversationMemory:
    """Stores sequential dialog turns and prunes older turns when exceeding token budgets."""

    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
        self.messages: List[Dict[str, str]] = []
        self.budget = TokenBudgetManager()

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        self._prune()

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        self._prune()

    def _total_tokens(self) -> int:
        return sum(self.budget.estimate_tokens(m["content"]) for m in self.messages)

    def _prune(self):
        """Evicts oldest turns from the front if token count exceeds max_tokens."""
        while self._total_tokens() > self.max_tokens and len(self.messages) > 1:
            self.messages.pop(0)

    def get_history(self) -> List[Dict[str, str]]:
        return list(self.messages)

    def clear(self):
        self.messages.clear()
