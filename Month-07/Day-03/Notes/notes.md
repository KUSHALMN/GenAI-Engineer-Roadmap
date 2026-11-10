# 📝 Notes — Day 03: Authorization & Behavioral Patterns

## 1. Multi-Tenant Authorization Invariants
- **Fail-Closed Default:** If a permission check encounters an unhandled exception or missing context, access is denied.
- **Tenant Context Propagation:** Tenant IDs must originate from verified cryptographic JWT claims, never from user-supplied query strings or body parameters.
- **Hierarchical Scopes:** Resource:Action format (e.g., `workspace:document:write`).
