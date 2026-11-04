"""
Incremental Document Indexing Engine
Implements SHA-256 content hashing and versioning to eliminate redundant embedding computation:
1. Detects unchanged chunks -> Preserves existing vector embeddings.
2. Detects modified chunks -> Computes new embeddings and updates index.
3. Detects deleted chunks -> Purges stale vectors from index.
4. Detects newly added chunks -> Embeds and registers into index.
"""

import hashlib
from typing import List, Dict, Any, Tuple


class IncrementalIndexer:
    def __init__(self):
        # Index store: chunk_id -> {"text": str, "content_hash": str, "embedding": List[float], "version": int}
        self.index_store: Dict[str, Dict[str, Any]] = {}
        self.embedding_calls_made = 0

    def _hash_content(self, text: str) -> str:
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    def _mock_embed(self, text: str) -> List[float]:
        self.embedding_calls_made += 1
        # 4-dim normalized hash vector for simulation
        words = text.split()
        return [float(len(words)), float(hash(text) % 100) / 100.0]

    def index_document(self, doc_id: str, chunks: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Incrementally synchronizes a document's chunks with the vector store.
        """
        incoming_chunk_ids = {c["chunk_id"] for c in chunks}
        current_doc_chunks = {cid: val for cid, val in self.index_store.items() if val.get("doc_id") == doc_id}

        unchanged = 0
        updated = 0
        added = 0
        deleted = 0

        # Step 1: Process incoming chunks
        for c in chunks:
            cid = c["chunk_id"]
            text = c["text"]
            c_hash = self._hash_content(text)

            if cid in current_doc_chunks:
                if current_doc_chunks[cid]["content_hash"] == c_hash:
                    # Unchanged: Do NOT re-embed!
                    unchanged += 1
                else:
                    # Modified: Re-embed and bump version
                    new_emb = self._mock_embed(text)
                    self.index_store[cid] = {
                        "doc_id": doc_id,
                        "text": text,
                        "content_hash": c_hash,
                        "embedding": new_emb,
                        "version": current_doc_chunks[cid]["version"] + 1
                    }
                    updated += 1
            else:
                # Brand new chunk
                new_emb = self._mock_embed(text)
                self.index_store[cid] = {
                    "doc_id": doc_id,
                    "text": text,
                    "content_hash": c_hash,
                    "embedding": new_emb,
                    "version": 1
                }
                added += 1

        # Step 2: Delete stale chunks belonging to doc_id that are no longer present
        for old_cid in current_doc_chunks:
            if old_cid not in incoming_chunk_ids:
                del self.index_store[old_cid]
                deleted += 1

        return {
            "doc_id": doc_id,
            "unchanged_chunks": unchanged,
            "updated_chunks": updated,
            "added_chunks": added,
            "deleted_chunks": deleted,
            "total_embedding_api_calls": self.embedding_calls_made
        }


if __name__ == "__main__":
    indexer = IncrementalIndexer()

    doc_id = "legal_agreement_v1"
    initial_chunks = [
        {"chunk_id": "ch_01", "text": "Clause 1: Confidentiality obligation expires in 3 years."},
        {"chunk_id": "ch_02", "text": "Clause 2: Jurisdiction is governed by the laws of California."},
        {"chunk_id": "ch_03", "text": "Clause 3: Arbitration will be conducted in San Francisco."}
    ]

    print("=== Run 1: Initial Ingestion ===")
    r1 = indexer.index_document(doc_id, initial_chunks)
    print(f"Added: {r1['added_chunks']}, Unchanged: {r1['unchanged_chunks']}, API Calls: {r1['total_embedding_api_calls']}")

    print("\n=== Run 2: Re-indexing with 1 modification and 1 deletion ===")
    # Modify Clause 1, keep Clause 2, delete Clause 3, add Clause 4
    updated_chunks = [
        {"chunk_id": "ch_01", "text": "Clause 1: Confidentiality obligation expires in 5 years."}, # modified
        {"chunk_id": "ch_02", "text": "Clause 2: Jurisdiction is governed by the laws of California."}, # unchanged
        {"chunk_id": "ch_04", "text": "Clause 4: Severability clause protects remainder of contract."} # added
    ]
    r2 = indexer.index_document(doc_id, updated_chunks)
    print(f"Unchanged: {r2['unchanged_chunks']}, Updated: {r2['updated_chunks']}, Added: {r2['added_chunks']}, Deleted: {r2['deleted_chunks']}")
    print(f"Total Cumulative API Calls: {r2['total_embedding_api_calls']} (Saved 1 redundant embedding!)")
