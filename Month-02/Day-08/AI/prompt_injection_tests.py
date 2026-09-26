"""
Prompt Injection Testing & Input Sanitization Suite.
Evaluates inputs against adversarial patterns, canary tokens, and jailbreak markers.
"""

import json
import re
from typing import Any, Dict, List, Tuple


class InputSanitizer:
    """Sanitizes user input before passing into LLM prompt templates."""

    INJECTION_PATTERNS = [
        r"(?i)ignore\s+(all\s+)?(previous\s+|prior\s+)?(instructions|rules)",
        r"(?i)disregard\s+(all\s+)?(previous\s+|prior\s+)?(instructions|rules)",
        r"(?i)you\s+are\s+now\s+(DAN|unconstrained|jailbroken)",
        r"(?i)output\s+(the\s+)?(entire\s+)?system\s+prompt",
        r"(?i)print\s+(the\s+)?initial\s+prompt",
        r"(?i)send\s+.*?\s+to\s+.*?\.(com|net|org)",
        r"(?i)rm\s+-rf|cat\s+/etc/shadow",
    ]

    @classmethod
    def detect_injection(cls, prompt: str) -> Tuple[bool, str]:
        """Detect prompt injection patterns."""
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, prompt):
                return True, pattern
        return False, ""

    @classmethod
    def sanitize(cls, prompt: str) -> str:
        """Escape control characters and wrap in strict XML delimiters."""
        clean = prompt.replace("```", "'''")
        return f"<user_query>\n{clean.strip()}\n</user_query>"


def run_security_test_suite(dataset_path: str) -> Dict[str, Any]:
    """Runs test suite across all entries in security_test_cases.jsonl."""
    total = 0
    passed = 0
    results = []

    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            case = json.loads(line)
            total += 1
            is_injected, pattern = InputSanitizer.detect_injection(case["prompt"])

            # If expected to block, detection should be True
            if case["expected_action"] in ("block", "sanitize_or_block"):
                case_passed = is_injected
            else:  # expected to allow
                case_passed = not is_injected

            if case_passed:
                passed += 1

            results.append({
                "id": case["id"],
                "threat": case["threat"],
                "detected": is_injected,
                "passed": case_passed,
            })

    defense_accuracy = (passed / total) * 100.0 if total > 0 else 0.0

    return {
        "total_test_cases": total,
        "passed": passed,
        "defense_accuracy_pct": round(defense_accuracy, 2),
        "results": results,
    }


if __name__ == "__main__":
    import os
    dataset = os.path.join(os.path.dirname(__file__), "security_test_cases.jsonl")
    report = run_security_test_suite(dataset)
    print("Security Benchmark Report:", json.dumps(report, indent=2))
    assert report["passed"] == report["total_test_cases"]
    print("All prompt injection tests passed successfully!")
