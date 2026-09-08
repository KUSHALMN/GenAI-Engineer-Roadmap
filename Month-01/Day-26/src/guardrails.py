import re
from typing import Tuple, Optional

class GuardrailsEngine:
    JAILBREAK_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"system\s*override",
        r"you\s+are\s+now\s+dan",
        r"do\s+anything\s+now",
        r"bypass\s+(safety|content)\s+filters"
    ]

    TOXIC_TERMS = {"hate", "kill", "attack", "exploit", "weaponize", "ransomware"}

    PII_REGEX_PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "API_KEY": r"(?:sk-[a-zA-Z0-9]{20,48}|AIza[0-9A-Za-z-_]{35})"
    }

    @classmethod
    def validate_input(cls, user_prompt: str) -> Tuple[bool, Optional[str]]:
        if len(user_prompt.strip()) == 0:
            return False, "Empty prompt rejected"
        for pattern in cls.JAILBREAK_PATTERNS:
            if re.search(pattern, user_prompt, re.IGNORECASE):
                return False, f"Prompt injection / jailbreak detected: matches pattern '{pattern}'"
        tokens = set(re.findall(r"\b\w+\b", user_prompt.lower()))
        matched = tokens.intersection(cls.TOXIC_TERMS)
        if matched:
            return False, f"Harmful content detected: {', '.join(matched)}"
        return True, None

    @classmethod
    def redact_pii(cls, text: str) -> str:
        redacted = text
        for label, pattern in cls.PII_REGEX_PATTERNS.items():
            redacted = re.sub(pattern, f"[REDACTED_{label}]", redacted)
        return redacted

    @classmethod
    def validate_output(cls, model_output: str) -> str:
        return cls.redact_pii(model_output)
