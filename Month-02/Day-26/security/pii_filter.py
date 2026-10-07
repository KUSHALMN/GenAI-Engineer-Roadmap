"""PII Redaction and Data Anonymization Filter."""
import re
from typing import Dict, Any, Tuple


class PIIFilter:
    """Detects and redacts sensitive Personally Identifiable Information (PII)."""

    PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "PHONE": r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "API_KEY": r"\b(?:sk-[a-zA-Z0-9]{32,}|ghp_[a-zA-Z0-9]{36}|AIza[0-9A-Za-z-_]{35})\b",
    }

    def __init__(self, mask_style: str = "[REDACTED_{TYPE}]"):
        self.mask_style = mask_style

    def scan_and_redact(self, text: str) -> Tuple[str, Dict[str, int]]:
        """Scans string, redacts PII instances, and returns sanitized text with audit counts."""
        redacted_text = text
        detections: Dict[str, int] = {}

        for pii_type, pattern in self.PATTERNS.items():
            matches = list(re.finditer(pattern, redacted_text))
            if matches:
                detections[pii_type] = len(matches)
                mask = self.mask_style.replace("{TYPE}", pii_type)
                redacted_text = re.sub(pattern, mask, redacted_text)

        return redacted_text, detections
