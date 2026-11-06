"""
Day 01: Agent Architecture and Tool Contract Design
Validates tool definitions against JSON schema specifications, ensuring
strict parameter typing, return schemas, side-effect declarations, and idempotency flags.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import json

@dataclass
class ToolParameter:
    name: str
    type_str: str
    description: str
    required: bool = True
    enum: Optional[List[Any]] = None

@dataclass
class ToolContract:
    name: str
    description: str
    parameters: Dict[str, ToolParameter]
    return_type: str
    is_idempotent: bool = False
    has_side_effects: bool = False
    rate_limit_per_minute: int = 60

    def to_json_schema(self) -> Dict[str, Any]:
        """Convert contract into standard OpenAPI / JSON Schema format."""
        properties = {}
        required = []
        for param_name, param in self.parameters.items():
            prop: Dict[str, Any] = {
                "type": param.type_str,
                "description": param.description
            }
            if param.enum:
                prop["enum"] = param.enum
            properties[param_name] = prop
            if param.required:
                required.append(param_name)

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            },
            "side_effects": self.has_side_effects,
            "idempotent": self.is_idempotent
        }

    def validate_call_arguments(self, args: Dict[str, Any]) -> List[str]:
        """Validate input arguments against the tool schema; returns error list."""
        errors = []
        for name, param in self.parameters.items():
            if param.required and name not in args:
                errors.append(f"Missing required argument: '{name}'")
            elif name in args:
                val = args[name]
                expected_type = param.type_str
                if expected_type == "string" and not isinstance(val, str):
                    errors.append(f"Argument '{name}' expected string, got {type(val).__name__}")
                elif expected_type == "integer" and not isinstance(val, int):
                    errors.append(f"Argument '{name}' expected integer, got {type(val).__name__}")
                elif expected_type == "number" and not isinstance(val, (int, float)):
                    errors.append(f"Argument '{name}' expected number, got {type(val).__name__}")
                elif expected_type == "boolean" and not isinstance(val, bool):
                    errors.append(f"Argument '{name}' expected boolean, got {type(val).__name__}")
                if param.enum and val not in param.enum:
                    errors.append(f"Argument '{name}' value {val} not in allowed enum {param.enum}")
        return errors

if __name__ == "__main__":
    search_tool = ToolContract(
        name="web_search",
        description="Searches index for relevant knowledge snippets.",
        parameters={
            "query": ToolParameter("query", "string", "Search query term", required=True),
            "max_results": ToolParameter("max_results", "integer", "Limit results", required=False)
        },
        return_type="array",
        is_idempotent=True,
        has_side_effects=False
    )
    
    schema = search_tool.to_json_schema()
    print("Generated Tool Schema:")
    print(json.dumps(schema, indent=2))
    
    # Validation tests
    valid_args = {"query": "vector databases", "max_results": 5}
    invalid_args = {"max_results": "ten"}
    
    assert len(search_tool.validate_call_arguments(valid_args)) == 0, "Valid arguments failed validation!"
    errs = search_tool.validate_call_arguments(invalid_args)
    assert len(errs) > 0, "Invalid arguments failed to trigger validation errors!"
    print(f"Validation successfully caught expected errors: {errs}")
    print("Day 01 AI Tool Contract Validator passed all tests.")
