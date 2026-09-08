import json
import re
from typing import Type, TypeVar, Tuple, Optional
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

class StructuredOutputValidator:
    @classmethod
    def clean_json_markdown(cls, raw: str) -> str:
        text = raw.strip()
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if fence_match:
            text = fence_match.group(1).strip()
        text = re.sub(r",\s*([\]}])", r"\1", text)
        return text

    @classmethod
    def repair_json(cls, raw: str) -> str:
        cleaned = cls.clean_json_markdown(raw)
        open_braces = cleaned.count("{") - cleaned.count("}")
        open_brackets = cleaned.count("[") - cleaned.count("]")
        if open_brackets > 0:
            cleaned += "]" * open_brackets
        if open_braces > 0:
            cleaned += "}" * open_braces
        return cleaned

    @classmethod
    def parse_and_validate(cls, raw: str, model_cls: Type[T]) -> Tuple[Optional[T], Optional[str]]:
        repaired = cls.repair_json(raw)
        try:
            data = json.loads(repaired)
        except json.JSONDecodeError as e:
            return None, f"JSONDecodeError: {str(e)}"

        try:
            instance = model_cls.model_validate(data)
            return instance, None
        except ValidationError as e:
            errors = [f"{' -> '.join(str(p) for p in err['loc'])}: {err['msg']}" for err in e.errors()]
            return None, "Validation failed: " + "; ".join(errors)
