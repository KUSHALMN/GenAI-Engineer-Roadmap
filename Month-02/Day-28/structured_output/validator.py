"""JSON output validator with automatic markdown block stripping and repair."""
import json
import re
from typing import Dict, Any, Type, Tuple


class OutputValidator:
    """Cleans backticks, fixes trailing commas, and validates model output."""

    @staticmethod
    def clean_json_string(raw_text: str) -> str:
        """Strip markdown code fence blocks if present."""
        cleaned = raw_text.strip()
        # Remove ```json ... ``` or ``` ... ```
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        # Strip trailing commas before closing braces/brackets
        cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)
        return cleaned.strip()

    @staticmethod
    def parse_and_validate(raw_text: str, required_keys: Tuple[str, ...]) -> Dict[str, Any]:
        cleaned = OutputValidator.clean_json_string(raw_text)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON: {str(e)} | Input: {raw_text[:100]}")

        if not isinstance(parsed, dict):
            raise ValueError(f"Expected JSON object dict, received {type(parsed).__name__}")

        for k in required_keys:
            if k not in parsed:
                raise ValueError(f"Missing mandatory key: '{k}'")

        return parsed
