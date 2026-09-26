"""
Tool Permission & Execution Policy Engine.
Enforces Role-Based Access Control (RBAC), argument validation,
and path traversal checks before executing agent tools.
"""

import os
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class Role(str, Enum):
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"


class ToolPermissionPolicy:
    """Enforces permissions and sandboxing for tool execution."""

    # Permission matrix: tool_name -> minimum required role
    PERMISSIONS: Dict[str, Role] = {
        "calculator": Role.GUEST,
        "search_web": Role.USER,
        "read_file": Role.USER,
        "write_file": Role.ADMIN,
        "execute_code": Role.ADMIN,
    }

    ROLE_HIERARCHY = {
        Role.GUEST: 1,
        Role.USER: 2,
        Role.ADMIN: 3,
    }

    ALLOWED_DIRECTORIES = ["/workspace", "./safe_data"]

    @classmethod
    def can_execute(cls, role: Role, tool_name: str) -> bool:
        """Check if role has sufficient authorization for tool."""
        required_role = cls.PERMISSIONS.get(tool_name)
        if not required_role:
            return False  # Deny by default for unregistered tools
        return cls.ROLE_HIERARCHY[role] >= cls.ROLE_HIERARCHY[required_role]

    @classmethod
    def validate_file_path(cls, path: str) -> bool:
        """Prevent path traversal vulnerabilities (e.g. ../../etc/passwd)."""
        normalized = os.path.normpath(path)
        if ".." in normalized or normalized.startswith("/") and not normalized.startswith("/workspace"):
            return False
        return True

    @classmethod
    def authorize_and_validate(cls, role: Role, tool_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """Verify role authorization and validate tool-specific arguments."""
        if not cls.can_execute(role, tool_name):
            return False, f"Permission Denied: Role '{role.value}' cannot execute tool '{tool_name}'"

        # Validate file paths if present
        if "path" in args and isinstance(args["path"], str):
            if not cls.validate_file_path(args["path"]):
                return False, f"Security Violation: Path traversal detected in '{args['path']}'"

        # Validate execute_code commands
        if tool_name == "execute_code" and "command" in args:
            cmd = args["command"].lower()
            dangerous_tokens = ["rm -rf", "drop table", "shutdown", "wget", "curl", ";", "|"]
            if any(tok in cmd for tok in dangerous_tokens):
                return False, f"Security Violation: Prohibited shell command token detected"

        return True, "Authorized"


if __name__ == "__main__":
    from typing import Tuple

    # Guest tries calculator -> OK
    ok, msg = ToolPermissionPolicy.authorize_and_validate(Role.GUEST, "calculator", {"expression": "2+2"})
    assert ok is True

    # User tries write_file -> DENIED
    ok, msg = ToolPermissionPolicy.authorize_and_validate(Role.USER, "write_file", {"path": "file.txt"})
    assert ok is False
    assert "Permission Denied" in msg

    # Admin tries path traversal -> DENIED
    ok, msg = ToolPermissionPolicy.authorize_and_validate(Role.ADMIN, "read_file", {"path": "../../etc/passwd"})
    assert ok is False
    assert "Path traversal" in msg

    print("Tool permission tests passed successfully!")
