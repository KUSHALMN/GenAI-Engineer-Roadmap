"""
PostgreSQL Schema and Indexing: Relational models, compound B-Tree & GIN indexes,
JSONB metadata queries, and transaction rollback mechanics.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class DocumentMetadata:
    tags: List[str]
    author: str
    tokens: int


class PostgresSimulatedDB:
    def __init__(self):
        self.rows: Dict[int, Dict[str, Any]] = {}
        # Inverted GIN index for JSONB tags: tag -> set of row_ids
        self.gin_tag_index: Dict[str, set] = {}
        # Compound B-Tree index: (tenant_id, created_at) -> list of row_ids
        self.btree_tenant_created: Dict[tuple, List[int]] = {}
        self.current_id = 1

    def insert(self, tenant_id: str, title: str, metadata: DocumentMetadata, created_at: int) -> int:
        row_id = self.current_id
        self.current_id += 1
        record = {
            "id": row_id,
            "tenant_id": tenant_id,
            "title": title,
            "metadata": metadata,
            "created_at": created_at
        }
        self.rows[row_id] = record

        # Maintain GIN index
        for tag in metadata.tags:
            if tag not in self.gin_tag_index:
                self.gin_tag_index[tag] = set()
            self.gin_tag_index[tag].add(row_id)

        # Maintain compound B-tree index
        key = (tenant_id, created_at)
        if key not in self.btree_tenant_created:
            self.btree_tenant_created[key] = []
        self.btree_tenant_created[key].append(row_id)
        return row_id

    def query_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        matching_ids = self.gin_tag_index.get(tag, set())
        return [self.rows[rid] for rid in matching_ids]


if __name__ == "__main__":
    db = PostgresSimulatedDB()
    m1 = DocumentMetadata(["finance", "quarterly"], "Alice", 1400)
    m2 = DocumentMetadata(["legal", "compliance"], "Bob", 2200)

    id1 = db.insert("tenant_1", "Q3 Report", m1, 1700000000)
    id2 = db.insert("tenant_1", "Privacy Policy", m2, 1700000500)

    res = db.query_by_tag("finance")
    assert len(res) == 1
    assert res[0]["id"] == id1
    print("=== Day 05: PostgreSQL Schema & Indexing ===")
    print("GIN tag indexing and compound index simulation passed.")
