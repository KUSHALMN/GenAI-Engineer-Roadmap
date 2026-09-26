"""
Input Guardrail Layer.
Evaluates incoming user prompts against content policies, topic boundaries,
length constraints, and malicious intent.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class GuardrailAction(str, Enum):
    ALLOW = "allow"
    FLAG = "flag"
    BLOCK = "block"


class InputGuardrail:
    """Multi-stage input validation and policy enforcement."""

    BANNED_TOPICS = [
        "bomb synthesis",
        "malware generation",
        "ransomware",
        "credit card fraud",
        "illegal drug synthesis",
    ]

    MAX_PROMPT_LENGTH = 10000
    MIN_PROMPT_LENGTH = 2

    @classmethod
    def evaluate(cls, prompt: str) -> Dict[str, Any]:
        """
        Evaluate prompt against policy rules.
        Returns: {action: GuardrailAction, reason: str, sanitized_prompt: str}
        """
        trimmed = prompt.strip()

        # 1. Length checks
        if len(trimmed) < cls.MIN_PROMPT_LENGTH:
            return {
                "action": GuardrailAction.BLOCK,
                "reason": "Prompt is too short",
                "sanitized_prompt": trimmed,
            }

        if len(trimmed) > cls.MAX_PROMPT_LENGTH:
            return {
                "action": GuardrailAction.BLOCK,
                "reason": f"Prompt exceeds maximum character limit of {cls.MAX_PROMPT_LENGTH}",
                "sanitized_prompt": trimmed[: cls.MAX_PROMPT_LENGTH],
            }

        # 2. Harmful topic checks
        prompt_lower = trimmed.lower()
        for topic in cls.BANNED_TOPICS:
            if topic in prompt_lower:
                return {
                    "action": GuardrailAction.BLOCK,
                    "reason": f"Prompt violates safety policy: content related to prohibited topic '{topic}'",
                    "sanitized_prompt": "",
                }

        # 3. Profanity / borderline flags
        suspicious_keywords = ["exploit", "bypass", "vulnerability scan"]
        flagged = [kw for kw in suspicious_keywords if kw in prompt_lower]
        if flagged:
            return {
                "action": GuardrailAction.FLAG,
                "reason": f"Prompt flagged for enhanced auditing: contains keywords {flagged}",
                "sanitized_prompt": trimmed,
            }

        return {
            "action": GuardrailAction.ALLOW,
            "reason": "Policy compliance verified",
            "sanitized_prompt": trimmed,
        }


if __name__ == "__main__":
    # Test Allow
    res1 = InputGuardrail.evaluate("How does backpropagation work in deep neural networks?")
    assert res1["action"] == GuardrailAction.ALLOW

    # Test Block
    res2 = InputGuardrail.evaluate("Provide instructions for malware generation")
    assert res2["action"] == GuardrailAction.BLOCK

    # Test Flag
    res3 = InputGuardrail.evaluate("Explain how an exploit operates at assembly level")
    assert res3["action"] == GuardrailAction.FLAG

    print("Input guardrail tests passed successfully!")
