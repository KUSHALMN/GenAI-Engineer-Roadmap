"""
Production API Architecture: Routers, Services, Repositories, Dependency Injection,
standard error envelopes, and paginated query results.
"""

from dataclasses import dataclass, field
import uuid
from typing import Any, Dict, List, Optional


@dataclass
class APIResponseEnvelope:
    success: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PaginationParams:
    page: int = 1
    page_size: int = 10

    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class DocumentRepository:
    def __init__(self):
        self._db: Dict[str, Dict[str, Any]] = {}

    def save(self, tenant_id: str, title: str, content: str) -> Dict[str, Any]:
        doc_id = str(uuid.uuid4())[:8]
        record = {
            "id": doc_id,
            "tenant_id": tenant_id,
            "title": title,
            "content": content
        }
        self._db[doc_id] = record
        return record

    def list_paginated(self, tenant_id: str, offset: int, limit: int) -> List[Dict[str, Any]]:
        tenant_docs = [doc for doc in self._db.values() if doc["tenant_id"] == tenant_id]
        return tenant_docs[offset:offset + limit]

    def count(self, tenant_id: str) -> int:
        return sum(1 for doc in self._db.values() if doc["tenant_id"] == tenant_id)


class DocumentService:
    def __init__(self, repo: DocumentRepository):
        self.repo = repo

    def ingest_document(self, tenant_id: str, title: str, content: str) -> APIResponseEnvelope:
        if not title.strip():
            return APIResponseEnvelope(
                success=False,
                error={"code": "VALIDATION_ERROR", "message": "Document title cannot be empty"}
            )
        record = self.repo.save(tenant_id, title, content)
        return APIResponseEnvelope(success=True, data=record)

    def get_documents(self, tenant_id: str, pagination: PaginationParams) -> APIResponseEnvelope:
        records = self.repo.list_paginated(tenant_id, pagination.offset(), pagination.page_size)
        total = self.repo.count(tenant_id)
        return APIResponseEnvelope(
            success=True,
            data=records,
            meta={"page": pagination.page, "page_size": pagination.page_size, "total_records": total}
        )


if __name__ == "__main__":
    repo = DocumentRepository()
    service = DocumentService(repo)

    res1 = service.ingest_document("tenant_alpha", "Architecture Spec", "Microservices with clean architecture")
    res2 = service.ingest_document("tenant_alpha", "API Guidelines", "Standard envelopes and pagination")
    assert res1.success is True

    paginated = service.get_documents("tenant_alpha", PaginationParams(page=1, page_size=10))
    print("=== Day 01: Production API Architecture ===")
    print(f"Status: Success={paginated.success}")
    print(f"Total Tenant Records: {paginated.meta['total_records']}")
    print(f"Sample Ingested Doc ID: {res1.data['id']}")
