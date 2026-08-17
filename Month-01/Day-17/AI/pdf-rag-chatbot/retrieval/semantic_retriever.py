from __future__ import annotations

from typing import Any, Dict, List
from app.embedding import embed_texts
from app.loader import Document
from app.vector_store import VectorStore


class SemanticRetriever:
    """Retrieves top-k documents based on vector cosine similarity."""

    def __init__(self, store: VectorStore | None = None):
        self.store = store or VectorStore()

    def index(self, documents: List[Document]) -> None:
        """Embed and add documents to the internal vector store."""
        if not documents:
            return
        texts = [doc.text for doc in documents]
        vectors = embed_texts(texts)
        for doc, vec in zip(documents, vectors):
            meta = dict(doc.metadata)
            meta["text"] = doc.text
            self.store.add(vec, meta)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve the most semantically relevant documents for a query."""
        if self.store.count() == 0 or not query.strip():
            return []
        query_vector = embed_texts([query])[0]
        return self.store.search(query_vector, top_k=top_k)

    def clear(self) -> None:
        """Clear indexed vectors."""
        self.store.clear()


# Default singleton instance
SEMANTIC_RETRIEVER = SemanticRetriever()


def index_semantic_documents(documents: List[Document]) -> None:
    SEMANTIC_RETRIEVER.index(documents)


def retrieve_semantic(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    return SEMANTIC_RETRIEVER.retrieve(query, top_k=top_k)
