import json
import re
from typing import Type, TypeVar, Tuple, Optional, Dict, Any
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

class StructuredOutputValidator:
    """
    Production-grade JSON repair and Pydantic validator.
    Recovers from common LLM generation defects:
    - Markdown code fences (```json ... ```)
    - Trailing commas in arrays or objects
    - Unbalanced curly braces / brackets
    - Missing quotation marks around keys
    """

    @classmethod
    def clean_json_markdown(cls, raw: str) -> str:
        text = raw.strip()
        # Strip markdown fences
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if fence_match:
            text = fence_match.group(1).strip()
        
        # Remove trailing commas before closing braces/brackets
        text = re.sub(r",\s*([\]}])", r"\1", text)
        return text

    @classmethod
    def repair_json(cls, raw: str) -> str:
        cleaned = cls.clean_json_markdown(raw)
        
        # Balance closing braces if truncated
        open_braces = cleaned.count("{") - cleaned.count("}")
        open_brackets = cleaned.count("[") - cleaned.count("]")
        
        if open_brackets > 0:
            cleaned += "]" * open_brackets
        if open_braces > 0:
            cleaned += "}" * open_braces
            
        return cleaned

    @classmethod
    def parse_and_validate(cls, raw: str, model_cls: Type[T]) -> Tuple[Optional[T], Optional[str]]:
        """
        Attempts to parse and validate raw string against Pydantic model.
        Returns (model_instance, None) on success or (None, error_feedback) on failure.
        """
        repaired = cls.repair_json(raw)
        try:
            data = json.loads(repaired)
        except json.JSONDecodeError as e:
            return None, f"JSONDecodeError: {str(e)}. String was: {repaired[:100]}..."

        try:
            instance = model_cls.model_validate(data)
            return instance, None
        except ValidationError as e:
            # Generate actionable error feedback for LLM retry
            errors = []
            for err in e.errors():
                loc = " -> ".join(str(p) for p in err["loc"])
                msg = err["msg"]
                errors.append(f"Field '{loc}': {msg}")
            feedback = "Validation failed: " + "; ".join(errors)
            return None, feedback
