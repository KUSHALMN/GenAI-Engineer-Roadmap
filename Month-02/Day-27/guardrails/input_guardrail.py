"""Input Guardrail: Intercepts toxic, injection, and sensitive user prompts."""
import re
from typing import Dict, Any
from .pii_detector import PIIDetector


class InputGuardrailException(Exception):
    pass


class InputGuardrail:
    """Pre-execution firewall screening user inputs before reaching foundation models."""

    BANNED_TOPICS = [
        r"(?i)\bhow\s+to\s+build\s+a\s+(bomb|weapon|explosive)",
        r"(?i)\bhack\s+into\s+(bank|system|database|account)",
        r"(?i)\bbypass\s+kyc\s+verification",
    ]

    def __init__(self):
        self.pii_detector = PIIDetector()

    def process(self, prompt: str) -> Dict[str, Any]:
        # 1. Banned harmful topics check
        for pattern in self.BANNED_TOPICS:
            if re.search(pattern, prompt):
                raise InputGuardrailException(f"Safety Policy Violation: Prohibited request topic detected.")

        # 2. PII scan
        pii_result = self.pii_detector.scan(prompt)
        if pii_result["has_pii"] and pii_result["max_severity"] >= 0.9:
            raise InputGuardrailException("Privacy Violation: High-severity PII detected in input.")

        return {
            "status": "APPROVED",
            "prompt": prompt,
            "pii_warnings": pii_result["findings"]
        }
