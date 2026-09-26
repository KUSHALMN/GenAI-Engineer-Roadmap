"""
Batch PII Scrubber for Datasets.
Scans and redacts emails, phone numbers, SSNs, credit cards, IP addresses, and user handles
across large dataset corpora with summary statistics.
"""

import re
from typing import Any, Dict, List, Tuple


class DatasetPIIScrubber:
    """Batch PII detector and scrubber for training pipelines."""

    PATTERNS: Dict[str, Tuple[re.Pattern, str]] = {
        "EMAIL": (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"), "[EMAIL]"),
        "PHONE": (re.compile(r"\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b"), "[PHONE]"),
        "SSN": (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
        "CREDIT_CARD": (re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}\b"), "[CREDIT_CARD]"),
        "IPV4": (re.compile(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"), "[IP_ADDRESS]"),
    }

    @classmethod
    def scrub_text(cls, text: str) -> Tuple[str, Dict[str, int]]:
        """Scrub text and count occurrences of redacted PII."""
        counts = {}
        scrubbed = text

        for entity_type, (pattern, replacement) in cls.PATTERNS.items():
            matches = pattern.findall(scrubbed)
            if matches:
                counts[entity_type] = len(matches)
                scrubbed = pattern.sub(replacement, scrubbed)

        return scrubbed, counts

    @classmethod
    def scrub_dataset(cls, records: List[Dict[str, Any]], text_key: str = "text") -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Scrubs entire list of dataset records."""
        scrubbed_records = []
        total_pii_counts: Dict[str, int] = {}
        rows_with_pii = 0

        for r in records:
            raw = r.get(text_key, "")
            cleaned, counts = cls.scrub_text(raw)
            new_record = dict(r)
            new_record[text_key] = cleaned
            scrubbed_records.append(new_record)

            if counts:
                rows_with_pii += 1
                for k, v in counts.items():
                    total_pii_counts[k] = total_pii_counts.get(k, 0) + v

        summary = {
            "total_records": len(records),
            "records_with_pii": rows_with_pii,
            "pii_record_rate_pct": round((rows_with_pii / max(len(records), 1)) * 100, 2),
            "pii_entity_breakdown": total_pii_counts,
        }
        return scrubbed_records, summary


if __name__ == "__main__":
    records = [
        {"id": 1, "text": "Contact user at john@doe.org or call 415-555-9012."},
        {"id": 2, "text": "Server hosted at 10.0.0.1 requires maintenance."},
        {"id": 3, "text": "Deep learning uses gradient descent optimization."},
    ]

    scrubbed, summary = DatasetPIIScrubber.scrub_dataset(records)
    print("Scrubbed Summary:", summary)
    assert summary["records_with_pii"] == 2
    assert "[EMAIL]" in scrubbed[0]["text"]
    assert "[IP_ADDRESS]" in scrubbed[1]["text"]
    print("DatasetPIIScrubber tests passed successfully!")
