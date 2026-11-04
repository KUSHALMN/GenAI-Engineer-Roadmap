"""
Multi-Tenant Filtered Hybrid Retriever
Demonstrates pre-filtering and post-filtering mechanisms:
- Multi-tenant boundary isolation (tenant_id)
- Department & Role-Based Access Control (RBAC) metadata filters
- Date range and document-type filters combined with hybrid score ranking
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class FilteredHybridRetriever:
    def __init__(self, corpus: List[Dict[str, Any]]):
        self.corpus = corpus

    def _matches_filters(self, doc_meta: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Evaluates strict equality, set containment, and date range filters"""
        # 1. Tenant boundary isolation (mandatory security check)
        if "tenant_id" in filters and doc_meta.get("tenant_id") != filters["tenant_id"]:
            return False

        # 2. Allowed departments check (RBAC)
        if "allowed_departments" in filters:
            if doc_meta.get("department") not in filters["allowed_departments"]:
                return False

        # 3. Document classification / type
        if "doc_type" in filters and doc_meta.get("doc_type") != filters["doc_type"]:
            return False

        # 4. Date range filter
        if "created_after" in filters:
            doc_date = datetime.strptime(doc_meta.get("created_at", "2000-01-01"), "%Y-%m-%d")
            min_date = datetime.strptime(filters["created_after"], "%Y-%m-%d")
            if doc_date < min_date:
                return False

        return True

    def search(self, query: str, filters: Dict[str, Any], top_k: int = 3) -> Dict[str, Any]:
        """
        Pre-filter execution: guarantees restricted tenant data never enters
        the candidate scoring stage.
        """
        q_tokens = set(query.lower().split())
        qualified_candidates = []
        rejected_count = 0

        for doc in self.corpus:
            meta = doc.get("metadata", {})
            if not self._matches_filters(meta, filters):
                rejected_count += 1
                continue

            # Calculate hybrid keyword relevance on authorized subset
            d_tokens = set(doc["text"].lower().split())
            score = len(q_tokens.intersection(d_tokens)) / max(1, len(q_tokens))
            qualified_candidates.append({
                "id": doc["id"],
                "text": doc["text"],
                "score": round(score, 3),
                "metadata": meta
            })

        qualified_candidates.sort(key=lambda x: x["score"], reverse=True)

        return {
            "query": query,
            "filters_applied": filters,
            "total_corpus_size": len(self.corpus),
            "filtered_out_docs": rejected_count,
            "returned_results": qualified_candidates[:top_k]
        }


if __name__ == "__main__":
    multi_tenant_corpus = [
        {
            "id": "c1",
            "text": "Acme Corp Q3 financial statements and EBITDA projections.",
            "metadata": {"tenant_id": "acme", "department": "finance", "doc_type": "report", "created_at": "2024-09-01"}
        },
        {
            "id": "c2",
            "text": "Acme Corp Kubernetes deployment configurations and VPC peering secrets.",
            "metadata": {"tenant_id": "acme", "department": "engineering", "doc_type": "infrastructure", "created_at": "2024-10-15"}
        },
        {
            "id": "c3",
            "text": "Beta Corp confidential customer list and quarterly renewals.",
            "metadata": {"tenant_id": "beta", "department": "sales", "doc_type": "report", "created_at": "2024-10-01"}
        },
        {
            "id": "c4",
            "text": "Acme Corp employee benefits guide and health insurance plans.",
            "metadata": {"tenant_id": "acme", "department": "hr", "doc_type": "handbook", "created_at": "2024-01-10"}
        }
    ]

    retriever = FilteredHybridRetriever(multi_tenant_corpus)

    # Search scenario: Acme Engineering user searching for deployment configs
    filters = {
        "tenant_id": "acme",
        "allowed_departments": ["engineering", "finance"],
        "created_after": "2024-06-01"
    }
    res = retriever.search("Kubernetes deployment configurations", filters=filters)

    print("=== Multi-Tenant Filtered Search Results ===")
    print(f"Total Corpus: {res['total_corpus_size']} | Filtered Out: {res['filtered_out_docs']}")
    for hit in res["returned_results"]:
        print(f"[{hit['id']}] Score: {hit['score']} (Tenant: {hit['metadata']['tenant_id']}, Dept: {hit['metadata']['department']})")
        print(f"Content: \"{hit['text']}\"")
