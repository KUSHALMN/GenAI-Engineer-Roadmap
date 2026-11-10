"""
Multi-Tenancy Data Isolation: Row-level tenant partitioning,
cross-tenant query filtering, and vector index isolation.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class DocumentRecord:
    id: str
    tenant_id: str
    vector: List[float]
    payload: Dict[str, Any]


class MultiTenantVectorIndex:
    def __init__(self):
        # Inverted index partitioned by tenant_id
        self._partitions: Dict[str, List[DocumentRecord]] = {}

    def insert(self, record: DocumentRecord):
        if record.tenant_id not in self._partitions:
            self._partitions[record.tenant_id] = []
        self._partitions[record.tenant_id].append(record)

    def search(self, caller_tenant_id: str, query_vector: List[float], top_k: int = 5) -> List[DocumentRecord]:
        # Enforce hard tenant isolation: caller cannot query other partitions
        partition = self._partitions.get(caller_tenant_id, [])
        # Simple dot product simulation
        scored = []
        for doc in partition:
            score = sum(q * d for q, d in zip(query_vector, doc.vector))
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:top_k]]


if __name__ == "__main__":
    idx = MultiTenantVectorIndex()
    idx.insert(DocumentRecord("doc_1", "tenant_alpha", [0.1, 0.9], {"title": "Alpha Confidential"}))
    idx.insert(DocumentRecord("doc_2", "tenant_beta", [0.1, 0.9], {"title": "Beta Secrets"}))

    alpha_results = idx.search("tenant_alpha", [0.1, 0.9], top_k=5)
    assert len(alpha_results) == 1
    assert alpha_results[0].id == "doc_1"

    # Verify Beta cannot see Alpha
    beta_results = idx.search("tenant_beta", [0.1, 0.9], top_k=5)
    assert len(beta_results) == 1
    assert beta_results[0].id == "doc_2"

    print("=== Day 04: Multi-Tenant Data Isolation ===")
    print("Vector partition isolation successfully verified.")
