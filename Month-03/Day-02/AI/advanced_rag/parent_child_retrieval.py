"""Parent-Child (Hierarchical Chunking) Document Indexer & Retriever."""
from typing import List, Dict, Any


class ParentChildRetriever:
    """Indexes small child chunks for embedding search, returning larger parent contexts for generation."""

    def __init__(self):
        self.parent_store: Dict[str, Dict[str, Any]] = {}
        self.child_store: List[Dict[str, Any]] = []

    def add_parent_document(self, parent_id: str, title: str, full_content: str, child_chunk_size: int = 100):
        self.parent_store[parent_id] = {"title": title, "content": full_content}
        
        words = full_content.split()
        for idx in range(0, len(words), child_chunk_size):
            child_chunk = " ".join(words[idx : idx + child_chunk_size])
            self.child_store.append({
                "parent_id": parent_id,
                "child_id": f"{parent_id}_c{idx // child_chunk_size}",
                "content": child_chunk
            })

    def search_parent(self, query: str) -> List[Dict[str, Any]]:
        q_tokens = set(query.lower().split())
        scored = []

        for child in self.child_store:
            child_tokens = set(child["content"].lower().split())
            overlap = len(q_tokens.intersection(child_tokens))
            scored.append((overlap, child["parent_id"]))

        scored.sort(key=lambda x: x[0], reverse=True)
        seen_parents = set()
        results = []

        for score, parent_id in scored:
            if parent_id not in seen_parents and score > 0:
                seen_parents.add(parent_id)
                results.append({"parent_id": parent_id, **self.parent_store[parent_id]})

        return results
