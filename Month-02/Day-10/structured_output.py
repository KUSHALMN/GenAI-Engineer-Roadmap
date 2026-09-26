"""
Structured Output Parser with Self-Correction Reflection Retry.
Validates LLM raw completions against Pydantic models.
If parsing fails, formats validation errors into a feedback prompt and retries.
"""

import json
import re
from typing import Any, Callable, Dict, Optional, Type, TypeVar
from pydantic import BaseModel, ValidationError
from schemas import CodeReviewReport


T = TypeVar("T", bound=BaseModel)


class StructuredOutputEngine:

    @staticmethod
    def extract_json(raw_text: str) -> str:
        """Extracts JSON substring."""
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
        if match:
            return match.group(1).strip()
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return raw_text[start : end + 1]
        return raw_text.strip()

    @classmethod
    def parse_with_reflection(
        cls,
        raw_output: str,
        model_cls: Type[T],
        llm_fix_caller: Optional[Callable[[str], str]] = None,
        max_retries: int = 2,
    ) -> T:
        """
        Attempts to parse completion into model_cls.
        If validation fails, generates a reflection prompt with exact error details.
        """
        current_text = raw_output

        for attempt in range(max_retries + 1):
            try:
                json_str = cls.extract_json(current_text)
                data = json.loads(json_str)
                return model_cls.model_validate(data)
            except (json.JSONDecodeError, ValidationError) as err:
                if attempt == max_retries or not llm_fix_caller:
                    raise err

                # Reflection prompt asking model to fix its formatting errors
                error_msg = str(err)
                reflection_prompt = (
                    f"Your previous response failed validation with error:\n{error_msg}\n"
                    f"Target Schema Definition: {model_cls.model_json_schema()}\n"
                    f"Please provide ONLY the corrected valid JSON object."
                )
                current_text = llm_fix_caller(reflection_prompt)

        raise RuntimeError("Failed to parse structured output within retry limit")


if __name__ == "__main__":
    valid_json = """
    {
        "repository": "test-repo",
        "overall_score": 8.5,
        "summary": "Solid foundation",
        "findings": [],
        "approved": true
    }
    """

    res = StructuredOutputEngine.parse_with_reflection(valid_json, CodeReviewReport)
    assert res.repository == "test-repo"
    assert res.overall_score == 8.5
    print("Structured output parsing passed successfully!")
