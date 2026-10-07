"""JSON Schema and Type Contract Validator for LLM Responses."""
import json
from typing import Dict, Any, List, Optional


class SchemaValidationError(Exception):
    pass


class SchemaValidator:
    """Validates that candidate dictionary conforms to required schema keys and types."""

    def __init__(self, schema: Dict[str, type]):
        self.schema = schema

    def validate(self, data: Any) -> Dict[str, Any]:
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                raise SchemaValidationError(f"Invalid JSON string format: {str(e)}")

        if not isinstance(data, dict):
            raise SchemaValidationError(f"Expected JSON object dict, got {type(data).__name__}")

        missing = []
        type_mismatches = []

        for key, expected_type in self.schema.items():
            if key not in data:
                missing.append(key)
            elif not isinstance(data[key], expected_type):
                type_mismatches.append(
                    f"Field '{key}' expected {expected_type.__name__}, got {type(data[key]).__name__}"
                )

        if missing or type_mismatches:
            errors = []
            if missing:
                errors.append(f"Missing keys: {missing}")
            if type_mismatches:
                errors.extend(type_mismatches)
            raise SchemaValidationError("; ".join(errors))

        return data
