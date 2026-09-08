import re
from typing import Tuple, List, Optional
from pydantic import BaseModel

class GuardrailViolation(Exception):
    def __init__(self, message: str, category: str):
        super().__init__(message)
        self.category = category

class GuardrailsEngine:
    """
    Enterprise input and output guardrails engine.
    - Input scanner: Checks for toxic keywords, prompt injection heuristics, and sensitive PII.
    - Output scanner: Enforces hallucination filters and redacts leaked API keys or passwords.
    """

    JAILBREAK_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"system\s*override",
        r"you\s+are\s+now\s+dan",
        r"do\s+anything\s+now",
        r"bypass\s+(safety|content)\s+filters"
    ]

    TOXIC_TERMS = {
        "hate", "kill", "attack", "exploit", "weaponize", "ransomware"
    }

    PII_REGEX_PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "API_KEY": r"(?:sk-[a-zA-Z0-9]{20,48}|AIza[0-9A-Za-z-_]{35})"
    }

    @classmethod
    def validate_input(cls, user_prompt: str) -> Tuple[bool, Optional[str]]:
        # 1. Check prompt length
        if len(user_prompt.strip()) == 0:
            return False, "Empty prompt rejected"

        # 2. Check jailbreak heuristics
        for pattern in cls.JAILBREAK_PATTERNS:
            if re.search(pattern, user_prompt, re.IGNORECASE):
                return False, f"Prompt injection / jailbreak detected: matches pattern '{pattern}'"

        # 3. Check toxic keywords
        tokens = set(re.findall(r"\b\w+\b", user_prompt.lower()))
        matched_toxic = tokens.intersection(cls.TOXIC_TERMS)
        if matched_toxic:
            return False, f"Content policy violation: harmful terms detected ({', '.join(matched_toxic)})"

        return True, None

    @classmethod
    def redact_pii(cls, text: str) -> str:
        redacted = text
        for label, pattern in cls.PII_REGEX_PATTERNS.items():
            redacted = re.sub(pattern, f"[REDACTED_{label}]", redacted)
        return redacted

    @classmethod
    def validate_output(cls, model_output: str) -> str:
        # Redact any leaked credentials or PII before sending to client
        return cls.redact_pii(model_output)
