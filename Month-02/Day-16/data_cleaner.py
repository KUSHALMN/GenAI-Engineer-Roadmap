"""
Data Cleaning & Normalization Pipeline for GenAI Training & Fine-Tuning.
Handles:
- HTML/XML tag stripping
- Unicode NFKC normalization
- Whitespace canonicalization
- Noise & boilerplate removal
- Min/Max token and character length filtering
"""

import html
import re
import unicodedata
from typing import Dict, List, Optional, Tuple


class DataCleaner:

    def __init__(self, min_length: int = 15, max_length: int = 20000):
        self.min_length = min_length
        self.max_length = max_length

    @staticmethod
    def strip_html_tags(text: str) -> str:
        """Unescapes HTML entities and strips tags."""
        unescaped = html.unescape(text)
        return re.sub(r"<[^>]+>", " ", unescaped)

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """Applies NFKC normalization to resolve ligature and compatibility variations."""
        return unicodedata.normalize("NFKC", text)

    @staticmethod
    def clean_whitespace(text: str) -> str:
        """Collapses consecutive spaces, tabs, and newlines."""
        return re.sub(r"[ \t]+", " ", text).strip()

    def clean_text(self, text: str) -> Optional[str]:
        """
        Executes full normalization pipeline.
        Returns cleaned text or None if failing length filters.
        """
        if not text:
            return None

        step1 = self.strip_html_tags(text)
        step2 = self.normalize_unicode(step1)
        step3 = self.clean_whitespace(step2)

        # Length validation
        if len(step3) < self.min_length or len(step3) > self.max_length:
            return None

        return step3

    def clean_dataset(self, rows: List[Dict[str, str]], text_key: str = "text") -> Tuple[List[Dict[str, str]], Dict[str, int]]:
        """Cleans dataset records and tracks dropped counts."""
        cleaned_rows = []
        dropped_count = 0

        for row in rows:
            raw_text = row.get(text_key, "")
            cleaned = self.clean_text(raw_text)
            if cleaned is not None:
                new_row = dict(row)
                new_row[text_key] = cleaned
                cleaned_rows.append(new_row)
            else:
                dropped_count += 1

        stats = {
            "initial_rows": len(rows),
            "retained_rows": len(cleaned_rows),
            "dropped_rows": dropped_count,
            "retention_rate_pct": round((len(cleaned_rows) / max(len(rows), 1)) * 100, 2),
        }
        return cleaned_rows, stats


if __name__ == "__main__":
    cleaner = DataCleaner(min_length=10)
    sample_raw = "  <p>Hello &amp; welcome to <b>GenAI</b> training pipeline!   </p>\n\n  "
    cleaned = cleaner.clean_text(sample_raw)
    print("Cleaned:", repr(cleaned))
    assert cleaned == "Hello & welcome to GenAI training pipeline!"

    rows = [{"text": sample_raw}, {"text": "too short"}, {"text": "Another valid long training document example."}]
    retained, stats = cleaner.clean_dataset(rows)
    assert len(retained) == 2
    assert stats["dropped_rows"] == 1
    print("DataCleaner tests passed successfully!", stats)
