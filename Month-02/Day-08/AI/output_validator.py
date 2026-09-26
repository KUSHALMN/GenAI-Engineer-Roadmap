"""
LLM Output Validator & Safety Filter.
Detects leaked system prompts, secret API keys, PII leaks, and prohibited outputs.
"""

import re
from typing import Any, Dict, List, Optional, Tuple


class OutputValidator:
    """Validates LLM generated content before returning to users."""

    # Regex patterns for high-risk data leakage
    SECRET_PATTERNS = [
        (r"sk-[a-zA-Z0-9]{32,}", "OpenAI API Key"),
        (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
        (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
        (r"(?i)password\s*[:=]\s*['\"][^'\"]+['\"]", "Exposed Password"),
    ]

    CANARY_TOKENS = ["CANARY_PROD_SECRET_XYZ991", "SYSTEM_INTERNAL_FLAG_882"]

    @classmethod
    def check_output_safety(cls, text: str, system_prompt: Optional[str] = None) -> Tuple[bool, List[str]]:
        """
        Inspect output for security risks.
        Returns: (is_safe, list_of_violations)
        """
        violations = []

        # 1. Canary Token Check
        for token in cls.CANARY_TOKENS:
            if token in text:
                violations.append(f"Critical: Canary token '{token}' leaked in output")

        # 2. Secret / API Key Check
        for pattern, desc in cls.SECRET_PATTERNS:
            if re.search(pattern, text):
                violations.append(f"Security Alert: Leaked credential ({desc})")

        # 3. System Prompt Leakage Check (N-gram overlap)
        if system_prompt and len(system_prompt.strip()) > 20:
            sys_words = system_prompt.strip().lower().split()
            # If 15+ consecutive words of system prompt appear in output
            if len(sys_words) >= 15:
                window_size = 12
                text_lower = text.lower()
                for i in range(len(sys_words) - window_size + 1):
                    ngram = " ".join(sys_words[i : i + window_size])
                    if ngram in text_lower:
                        violations.append("Confidentiality Violation: Verbatim system prompt leak detected")
                        break

        is_safe = len(violations) == 0
        return is_safe, violations

    @classmethod
    def redact_secrets(cls, text: str) -> str:
        """Replace discovered secrets with redaction placeholder."""
        redacted = text
        for pattern, _ in cls.SECRET_PATTERNS:
            redacted = re.sub(pattern, "[REDACTED_SECRET]", redacted)
        return redacted


if __name__ == "__main__":
    validator = OutputValidator()

    # Leaked key
    safe, viols = validator.check_output_safety("Here is the key: sk-abcdef1234567890abcdef1234567890")
    assert safe is False
    assert any("OpenAI API Key" in v for v in viols)

    # Leaked canary
    safe, viols = validator.check_output_safety("Debug output: CANARY_PROD_SECRET_XYZ991 found")
    assert safe is False
    assert any("Canary token" in v for v in viols)

    # Clean text
    safe, viols = validator.check_output_safety("Vector search uses cosine similarity.")
    assert safe is True
    assert len(viols) == 0

    print("Output validator tests passed successfully!")
