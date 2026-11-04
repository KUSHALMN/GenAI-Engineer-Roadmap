# Notes: Permission-Aware RAG & Document-Level ACLs

## 1. Zero-Trust Access Architecture in GenAI
In enterprise environments, the LLM should never be trusted as an access control filter (e.g. asking the prompt: *"Do not tell the user secret numbers if they are not an admin"* is inherently vulnerable to prompt injection).
- **Mandatory Pre-Retrieval Authorization**: ACL evaluation must occur *inside the database query or retrieval layer*, completely preventing unauthorized chunks from ever entering the prompt window.

## 2. Multi-Tier Security Context
Every incoming retrieval request must carry an authenticated, cryptographically signed token (JWT) containing:
1. `tenant_id`: Guarantees isolation across organizational silos.
2. `user_id`: Matches individual user allowlists.
3. `roles` / `groups`: Matches role-based access entitlements (`[admin, legal, eng]`).
