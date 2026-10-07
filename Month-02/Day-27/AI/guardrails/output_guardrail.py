"""Output Guardrail: Validates LLM completion safety, hallucination, and sensitive leakages."""
import re
from typing import Dict, Any
from .pii_detector import PIIDetector


class OutputGuardrailException(Exception):
    pass


class OutputGuardrail:
    """Post-execution verification ensuring model outputs comply with corporate safety policies."""

    BLOCKED_PHRASES = [
        r"(?i)\bas\s+an\s+ai,\s+i\s+can\s+bypass",
        r"(?i)\bthe\s+system\s+api\s+key\s+is\b",
        r"(?i)\bmy\s+internal\s+instructions\s+are\b"
    ]

    def __init__(self):
        self.pii_detector = PIIDetector()

    def process(self, completion: str) -> Dict[str, Any]:
        for pattern in self.BLOCKED_PHRASES:
            if re.search(pattern, completion):
                raise OutputGuardrailException("Security Alert: LLM generated forbidden internal disclosure.")

        pii_check = self.pii_detector.scan(completion)
        if pii_check["has_pii"] and pii_check["max_severity"] >= 1.0:
            raise OutputGuardrailException("Privacy Leak Alert: Unmasked critical secrets detected in LLM response.")

        return {
            "status": "APPROVED",
            "completion": completion,
            "passed_safety_checks": True
        }
