import re
from typing import Dict, Any

class DynamicModelRouter:
    """
    Intelligent Model Router:
    - Analyzes intent, prompt complexity, and token length.
    - Routes simple lookups / classification -> lightweight models (fast, cheap).
    - Routes complex math, multi-step code, or architectural reasoning -> frontier reasoning models.
    """

    COMPLEX_INTENT_PATTERNS = [
        r"\b(code|function|algorithm|class|refactor|debug)\b",
        r"\b(architecture|system design|scalability|tradeoffs)\b",
        r"\b(derive|proof|calculate|mathematics)\b"
    ]

    LIGHTWEIGHT_MODEL = "gpt-4o-mini"
    FRONTIER_MODEL = "gpt-4o"

    @classmethod
    def route_request(cls, prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        word_count = len(prompt.split())

        # Check for complex intent keywords
        is_complex = any(re.search(pat, prompt_lower) for pat in cls.COMPLEX_INTENT_PATTERNS)
        
        # Heavy prompts (>150 words) also route to frontier
        if is_complex or word_count > 150:
            return {
                "selected_model": cls.FRONTIER_MODEL,
                "tier": "frontier_reasoning",
                "reason": "Complex intent or large context detected"
            }

        return {
            "selected_model": cls.LIGHTWEIGHT_MODEL,
            "tier": "fast_lightweight",
            "reason": "Standard conversational or low-complexity query"
        }
