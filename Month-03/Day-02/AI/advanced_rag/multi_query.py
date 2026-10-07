"""Multi-Query Generator: Creates multiple diverse sub-queries to maximize recall."""
from typing import List


class MultiQueryGenerator:
    """Expands a single user prompt into multiple perspective queries."""

    def generate(self, user_query: str) -> List[str]:
        # Generates alternative lexical formulations
        variations = [
            user_query,
            f"Technical architecture overview of {user_query}",
            f"Key mechanisms and algorithms behind {user_query}",
            f"Best practices and trade-offs for {user_query}"
        ]
        return variations
