"""
PII (Personally Identifiable Information) Detector & Anonymizer.
Detects, masks, and pseudo-anonymizes emails, phone numbers, SSNs, credit cards, and IPs.
"""

import re
from typing import Dict, List, Tuple


class PIIDetector:
    """Detects and redacts sensitive PII entities."""

    PATTERNS: Dict[str, str] = {
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
        "PHONE": r"\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
        "IPV4": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
    }

    @classmethod
    def detect(cls, text: str) -> List[Dict[str, str]]:
        """Identify all PII spans in the input text."""
        findings = []
        for entity_type, pattern in cls.PATTERNS.items():
            for match in re.finditer(pattern, text):
                findings.append({
                    "entity_type": entity_type,
                    "value": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                })
        return findings

    @classmethod
    def redact(cls, text: str, placeholder_style: str = "token") -> Tuple[str, Dict[str, str]]:
        """
        Redacts PII.
        If placeholder_style == 'token': returns text with <EMAIL_1>, <PHONE_1> and mapping dict for de-anonymization.
        If placeholder_style == 'mask': returns text masked with [REDACTED_TYPE].
        """
        redacted_text = text
        mapping: Dict[str, str] = {}
        entity_counters: Dict[str, int] = {}

        # Scan all occurrences
        all_findings = cls.detect(text)
        # Sort descending by start position to avoid offset corruption during replacement
        all_findings.sort(key=lambda x: x["start"], reverse=True)

        for item in all_findings:
            etype = item["entity_type"]
            val = item["value"]
            start = item["start"]
            end = item["end"]

            entity_counters[etype] = entity_counters.get(etype, 0) + 1
            if placeholder_style == "token":
                token = f"<{etype}_{entity_counters[etype]}>"
                mapping[token] = val
                redacted_text = redacted_text[:start] + token + redacted_text[end:]
            else:
                redacted_text = redacted_text[:start] + f"[{etype}]" + redacted_text[end:]

        return redacted_text, mapping

    @staticmethod
    def deanonymize(text: str, mapping: Dict[str, str]) -> str:
        """Restores original PII values from tokens."""
        restored = text
        for token, original in mapping.items():
            restored = restored.replace(token, original)
        return restored


if __name__ == "__main__":
    sample = "Contact Alice at alice@example.com or 415-555-2671. Her SSN is 123-45-6789 and server is 192.168.1.10."
    findings = PIIDetector.detect(sample)
    assert len(findings) == 4

    # Test reversible tokenization
    redacted, map_dict = PIIDetector.redact(sample, placeholder_style="token")
    assert "alice@example.com" not in redacted
    assert "123-45-6789" not in redacted

    restored = PIIDetector.deanonymize(redacted, map_dict)
    assert restored == sample

    print("PII Detector & Redactor tests passed successfully!")
