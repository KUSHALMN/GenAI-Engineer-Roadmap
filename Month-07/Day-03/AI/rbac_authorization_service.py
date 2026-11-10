"""
Authorization and RBAC: Role-Based Access Control, Tenant Boundary Checks,
Fine-Grained Scopes, and Resource Ownership Verification.
"""

from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class UserContext:
    user_id: str
    tenant_id: str
    roles: List[str]


class RBACAuthorizationService:
    def __init__(self):
        # Role -> Allowed Actions
        self.role_permissions: Dict[str, Set[str]] = {
            "viewer": {"document:read", "model:query"},
            "editor": {"document:read", "document:write", "model:query"},
            "admin": {"document:read", "document:write", "document:delete", "model:query", "tenant:manage"}
        }

    def has_permission(self, context: UserContext, required_action: str) -> bool:
        for role in context.roles:
            if required_action in self.role_permissions.get(role, set()):
                return True
        return False

    def can_access_resource(self, context: UserContext, resource_tenant_id: str, action: str) -> bool:
        # Cross-tenant boundary check: STRICT isolation
        if context.tenant_id != resource_tenant_id:
            return False
        return self.has_permission(context, action)


if __name__ == "__main__":
    rbac = RBACAuthorizationService()
    user_alice = UserContext("alice", "tenant_a", ["editor"])
    user_bob = UserContext("bob", "tenant_b", ["admin"])

    assert rbac.can_access_resource(user_alice, "tenant_a", "document:write") is True
    assert rbac.can_access_resource(user_alice, "tenant_a", "document:delete") is False
    assert rbac.can_access_resource(user_bob, "tenant_a", "document:read") is False # Cross tenant blocked!

    print("=== Day 03: RBAC Authorization Service ===")
    print("Multi-tenant permission and isolation checks passed.")
