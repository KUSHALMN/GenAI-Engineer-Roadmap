"""Token Budget Manager: Partitions fixed context windows among System, Chat History, and RAG."""
from typing import Dict, Any


class TokenBudgetManager:
    """Allocates context window quotas dynamically."""

    def __init__(
        self,
        max_context_tokens: int = 8192,
        system_reserved: int = 1000,
        output_reserved: int = 2048,
        retrieval_reserved: int = 3000
    ):
        self.max_context_tokens = max_context_tokens
        self.system_reserved = system_reserved
        self.output_reserved = output_reserved
        self.retrieval_reserved = retrieval_reserved
        # Remainder is available for conversation memory history
        self.history_budget = max_context_tokens - (system_reserved + output_reserved + retrieval_reserved)

    def estimate_tokens(self, text: str) -> int:
        """Approximates tokens (4 characters per token)."""
        return max(1, len(text) // 4) if text else 0

    def get_budget_allocation(self) -> Dict[str, int]:
        return {
            "max_context": self.max_context_tokens,
            "system_reserved": self.system_reserved,
            "output_reserved": self.output_reserved,
            "retrieval_reserved": self.retrieval_reserved,
            "history_budget": self.history_budget
        }
