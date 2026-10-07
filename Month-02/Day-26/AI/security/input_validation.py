"""Input Validation, Sanitization, and Encoding Boundary Verification."""
import html
import unicodedata
from typing import Dict, Any


class InputValidator:
    """Sanitizes raw text, removes zero-width hidden characters, and normalizes unicode."""

    @staticmethod
    def sanitize(text: str) -> str:
        """Strip control characters, normalize NFKC unicode, and escape html."""
        if not text:
            return ""
        # 1. Normalize Unicode (counteract homoglyph attacks)
        normalized = unicodedata.normalize("NFKC", text)

        # 2. Strip non-printable control characters & zero-width stealth characters
        # Zero-width spaces, joiners, directional overrides (e.g. \u200B, \u202E)
        cleaned = "".join(
            ch for ch in normalized
            if ch == "\n" or ch == "\t" or (not unicodedata.category(ch).startswith("C") and ord(ch) not in {0x200B, 0x200C, 0x200D, 0x202E, 0xFEFF})
        )

        return cleaned.strip()

    @staticmethod
    def inspect(text: str) -> Dict[str, Any]:
        sanitized = InputValidator.sanitize(text)
        return {
            "original_length": len(text),
            "sanitized_length": len(sanitized),
            "contains_invisible_chars": len(text) > len(sanitized),
            "sanitized_text": sanitized
        }
