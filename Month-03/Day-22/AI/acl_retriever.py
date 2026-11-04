"""
Permission-Aware RAG Engine with Document-Level Access Control Lists (ACLs)
Applies strict authorization gates before evidence reaches the LLM context:
1. User-specific ACLs (e.g. read permissions by user_id)
2. Role-Based Access Control (e.g. 'admin', 'auditor', 'engineer')
3. Tenant isolation (strictly enforcing organization boundaries)
4. Negative security test cases verifying unauthorized data rejection
"""

from typing import List, Dict, Any, Set


class UserSecurityContext:
    def __init__(self, user_id: str, tenant_id: str, roles: List[str]):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.roles = set(roles)


class ACLRetriever:
    def __init__(self, corpus: List[Dict[str, Any]]):
        self.corpus = corpus

    def is_authorized(self, user: UserSecurityContext, doc: Dict[str, Any]) -> bool:
        meta = doc.get("metadata", {})

        # Security Check 1: Tenant Boundary (Hard requirement)
        if meta.get("tenant_id") != user.tenant_id:
            return False

        # Security Check 2: Direct user ACL allowlist
        allowed_users = meta.get("allowed_users", [])
        if user.user_id in allowed_users:
            return True

        # Security Check 3: Role / Group membership
        allowed_roles = set(meta.get("allowed_roles", []))
        if user.roles.intersection(allowed_roles):
            return True

        # If document is marked strictly public within tenant
        if meta.get("is_public_in_tenant", False):
            return True

        return False

    def retrieve_secure(
        self,
        query: str,
        user: UserSecurityContext,
        top_k: int = 3
    ) -> Dict[str, Any]:
        q_tokens = set(query.lower().split())
        authorized_hits = []
        denied_count = 0

        for doc in self.corpus:
            if not self.is_authorized(user, doc):
                denied_count += 1
                continue

            d_tokens = set(doc["text"].lower().split())
            score = len(q_tokens.intersection(d_tokens)) / max(1, len(q_tokens))
            authorized_hits.append({
                "id": doc["id"],
                "text": doc["text"],
                "relevance": round(score, 3),
                "metadata": doc.get("metadata", {})
            })

        authorized_hits.sort(key=lambda x: x["relevance"], reverse=True)

        return {
            "user_id": user.user_id,
            "tenant_id": user.tenant_id,
            "total_corpus_searched": len(self.corpus),
            "unauthorized_chunks_blocked": denied_count,
            "authorized_results": authorized_hits[:top_k]
        }


if __name__ == "__main__":
    secured_documents = [
        {
            "id": "doc_hr_salaries",
            "text": "Executive compensation packages and stock option vesting schedules for Q4.",
            "metadata": {"tenant_id": "corp_a", "allowed_roles": ["hr_exec", "c_level"]}
        },
        {
            "id": "doc_eng_architecture",
            "text": "Production Kubernetes cluster deployment specs and database connection strings.",
            "metadata": {"tenant_id": "corp_a", "allowed_roles": ["engineer", "admin"]}
        },
        {
            "id": "doc_public_handbook",
            "text": "Company holiday schedule and standard office remote work policy.",
            "metadata": {"tenant_id": "corp_a", "is_public_in_tenant": True}
        },
        {
            "id": "doc_tenant_b_secret",
            "text": "Confidential patent filings for external tenant Corp B.",
            "metadata": {"tenant_id": "corp_b", "is_public_in_tenant": True}
        }
    ]

    retriever = ACLRetriever(secured_documents)

    # User 1: Regular engineer in Corp A
    eng_user = UserSecurityContext(user_id="user_101", tenant_id="corp_a", roles=["engineer"])
    res1 = retriever.retrieve_secure("Kubernetes deployment and salary compensation", eng_user)

    print("=== Scenario 1: Engineer Search ===")
    print(f"Blocked Chunks: {res1['unauthorized_chunks_blocked']}")
    for r in res1["authorized_results"]:
        print(f"  * [{r['id']}] {r['text'][:55]}...")

    # Negative Test: Cross-tenant access attempt
    print("\n=== Scenario 2: Cross-Tenant Isolation Test ===")
    assert not any(r["id"] == "doc_tenant_b_secret" for r in res1["authorized_results"]), "SECURITY BREACH: Cross-tenant leak!"
    assert not any(r["id"] == "doc_hr_salaries" for r in res1["authorized_results"]), "SECURITY BREACH: Unauthorized HR access!"
    print("Negative security checks PASSED: No unauthorized or cross-tenant data leaked.")
