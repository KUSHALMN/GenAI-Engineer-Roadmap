"""Contextual PII Detector with Severity Scoring."""
import re
from typing import Dict, Any, List


class PIIDetector:
    """Scans and scores confidential records across email, phones, and API keys."""

    REGEX_RULES = {
        "EMAIL": (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", 0.7),
        "PHONE": (r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", 0.6),
        "CREDIT_CARD": (r"\b(?:\d{4}[-\s]?){3}\d{4}\b", 1.0),
        "AUTH_SECRET": (r"\b(?:Bearer\s+[a-zA-Z0-9_\-\.]{20,}|sk-[a-zA-Z0-9]{32,})\b", 1.0),
    }

    def scan(self, text: str) -> Dict[str, Any]:
        findings = []
        max_severity = 0.0

        for category, (pattern, severity) in self.REGEX_RULES.items():
            matches = re.findall(pattern, text)
            if matches:
                findings.append({"category": category, "count": len(matches), "severity": severity})
                max_severity = max(max_severity, severity)

        return {
            "has_pii": len(findings) > 0,
            "max_severity": max_severity,
            "findings": findings
        }
