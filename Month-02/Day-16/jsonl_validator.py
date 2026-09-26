"""
JSONL Dataset Validator for Fine-Tuning & Instruction Datasets.
Checks schema constraints, role integrity, empty strings, and localized syntax errors.
"""

import json
from typing import Any, Dict, List, Optional, Tuple


class JSONLValidator:
    """Validates instruction/chat JSONL datasets."""

    ALLOWED_ROLES = {"system", "user", "assistant"}

    @classmethod
    def validate_line(cls, line_num: int, line_content: str) -> Tuple[bool, Optional[str]]:
        """Validates a single line of JSONL."""
        trimmed = line_content.strip()
        if not trimmed:
            return False, f"Line {line_num}: Empty line"

        try:
            data = json.loads(trimmed)
        except json.JSONDecodeError as e:
            return False, f"Line {line_num}: Invalid JSON syntax ({e})"

        if not isinstance(data, dict):
            return False, f"Line {line_num}: Root element must be a JSON object"

        # Format 1: Chat format {"messages": [{"role": "user", "content": "..."}]}
        if "messages" in data:
            messages = data["messages"]
            if not isinstance(messages, list) or len(messages) < 2:
                return False, f"Line {line_num}: 'messages' must be a list with at least 2 turns"

            has_user = False
            has_assistant = False

            for idx, msg in enumerate(messages):
                if not isinstance(msg, dict):
                    return False, f"Line {line_num} Turn {idx}: Message must be an object"
                role = msg.get("role")
                content = msg.get("content")

                if role not in cls.ALLOWED_ROLES:
                    return False, f"Line {line_num} Turn {idx}: Invalid role '{role}'"
                if not content or not isinstance(content, str) or not content.strip():
                    return False, f"Line {line_num} Turn {idx}: Message content cannot be empty"

                if role == "user":
                    has_user = True
                elif role == "assistant":
                    has_assistant = True

            if not has_user or not has_assistant:
                return False, f"Line {line_num}: Dialogue must contain at least one user and one assistant message"

            return True, None

        # Format 2: Completion format {"prompt": "...", "completion": "..."}
        if "prompt" in data and "completion" in data:
            p = data["prompt"]
            c = data["completion"]
            if not isinstance(p, str) or not p.strip():
                return False, f"Line {line_num}: 'prompt' cannot be empty"
            if not isinstance(c, str) or not c.strip():
                return False, f"Line {line_num}: 'completion' cannot be empty"
            return True, None

        return False, f"Line {line_num}: Must contain either 'messages' or ('prompt' and 'completion') keys"

    @classmethod
    def validate_file_content(cls, lines: List[str]) -> Dict[str, Any]:
        """Validates all lines and produces comprehensive audit report."""
        total_lines = len(lines)
        valid_lines = 0
        errors = []

        for idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            is_valid, err = cls.validate_line(idx, line)
            if is_valid:
                valid_lines += 1
            else:
                errors.append(err)

        return {
            "total_lines": total_lines,
            "valid_lines": valid_lines,
            "invalid_lines": len(errors),
            "valid_rate_pct": round((valid_lines / max(total_lines, 1)) * 100, 2),
            "errors": errors[:10],  # sample up to 10 errors
        }


if __name__ == "__main__":
    sample_dataset = [
        json.dumps({"messages": [{"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hi there!"}]}),
        json.dumps({"prompt": "Summarize this article", "completion": "Article summary here."}),
        json.dumps({"messages": [{"role": "bad_role", "content": "Fail"}]}),  # invalid role
        '{"invalid_json": true,',  # syntax error
    ]

    report = JSONLValidator.validate_file_content(sample_dataset)
    print("Validation Report:", json.dumps(report, indent=2))
    assert report["valid_lines"] == 2
    assert report["invalid_lines"] == 2
    print("JSONLValidator tests passed successfully!")
