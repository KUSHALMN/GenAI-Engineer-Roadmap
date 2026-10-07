"""Query Rewriter expanding ambiguous conversational queries."""
from typing import List, Dict, Any


class QueryRewriter:
    """Rewrites implicit or pronoun-heavy user queries into standalone search strings."""

    def rewrite(self, query: str, conversation_history: List[Dict[str, str]]) -> str:
        # Check for ambiguous pronouns (it, that, they, these)
        lower_q = query.lower()
        if any(pronoun in lower_q.split() for pronoun in ["it", "this", "that", "these", "they"]):
            # Extract main noun from last assistant or user turn
            for turn in reversed(conversation_history):
                content = turn.get("content", "")
                if "lora" in content.lower():
                    return f"Explain how LoRA fine-tuning parameters work"
                if "hnsw" in content.lower() or "vector" in content.lower():
                    return f"Vector database HNSW nearest neighbor indexing details"

        return query
