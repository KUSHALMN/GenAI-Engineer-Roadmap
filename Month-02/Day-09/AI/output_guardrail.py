"""
Schema-Based Output Guardrail.
Validates LLM JSON output against strict schema models, enforces constraints,
and extracts markdown codeblocks automatically.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple, Type


class OutputValidationError(Exception):
    pass


class OutputGuardrail:
    """Enforces JSON structure and field validation on generated completions."""

    @staticmethod
    def extract_json_block(text: str) -> str:
        """Extracts JSON substring from markdown backticks or raw response."""
        # Try ```json ... ```
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            return match.group(1).strip()
        # Try finding outermost { ... }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start : end + 1]
        return text.strip()

    @classmethod
    def validate_schema(
        cls,
        raw_text: str,
        required_fields: List[str],
        field_types: Optional[Dict[str, Type]] = None,
        numeric_bounds: Optional[Dict[str, Tuple[float, float]]] = None,
    ) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Validates JSON schema, types, and bounds.
        Returns: (is_valid, parsed_dict, error_message)
        """
        json_str = cls.extract_json_block(raw_text)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            return False, None, f"JSON parsing failed: {e}"

        if not isinstance(data, dict):
            return False, None, "Expected JSON object at top level"

        # Check required fields
        for field in required_fields:
            if field not in data:
                return False, None, f"Missing required field: '{field}'"

        # Check types
        if field_types:
            for field, expected_type in field_types.items():
                if field in data and not isinstance(data[field], expected_type):
                    return False, None, f"Field '{field}' expected type {expected_type.__name__}, got {type(data[field]).__name__}"

        # Check numeric bounds
        if numeric_bounds:
            for field, (low, high) in numeric_bounds.items():
                if field in data and isinstance(data[field], (int, float)):
                    val = data[field]
                    if not (low <= val <= high):
                        return False, None, f"Field '{field}' value {val} out of bounds [{low}, {high}]"

        return True, data, "Valid"


if __name__ == "__main__":
    valid_llm_output = """
    Here is the requested analysis:
    ```json
    {
        "status": "success",
        "confidence": 0.95,
        "summary": "Data pipeline operational"
    }
    ```
    """

    ok, parsed, err = OutputGuardrail.validate_schema(
        raw_text=valid_llm_output,
        required_fields=["status", "confidence", "summary"],
        field_types={"status": str, "confidence": float, "summary": str},
        numeric_bounds={"confidence": (0.0, 1.0)},
    )
    assert ok is True
    assert parsed["confidence"] == 0.95

    # Invalid output (out of bounds)
    invalid_llm_output = '{"status": "success", "confidence": 1.5, "summary": "High"}'
    ok_bad, _, err_bad = OutputGuardrail.validate_schema(
        raw_text=invalid_llm_output,
        required_fields=["status", "confidence", "summary"],
        numeric_bounds={"confidence": (0.0, 1.0)},
    )
    assert ok_bad is False
    assert "out of bounds" in err_bad

    print("Output guardrail schema validation passed successfully!")
