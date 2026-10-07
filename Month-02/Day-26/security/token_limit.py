"""Input token limit enforcement and Denial of Service (DoS) protection."""
import re
from typing import Dict, Any


class TokenLimitException(Exception):
    """Raised when incoming prompt exceeds maximum allowable token ceiling."""
    pass


class TokenLimitGuard:
    """Enforces upper limits on prompt length to protect against resource exhaustion."""

    def __init__(self, max_tokens: int = 4000, chars_per_token_ratio: float = 4.0):
        self.max_tokens = max_tokens
        self.chars_per_token_ratio = chars_per_token_ratio

    def estimate_tokens(self, text: str) -> int:
        """Heuristic token estimation based on whitespace & punctuation splits."""
        if not text:
            return 0
        words = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
        return max(1, len(words))

    def validate(self, text: str) -> Dict[str, Any]:
        """Validate text against token limit."""
        estimated = self.estimate_tokens(text)
        if estimated > self.max_tokens:
            raise TokenLimitException(
                f"Prompt token count ({estimated}) exceeds maximum threshold ({self.max_tokens})"
            )
        return {
            "estimated_tokens": estimated,
            "max_tokens": self.max_tokens,
            "within_limit": True
        }
