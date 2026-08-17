from __future__ import annotations

import re
from typing import List
from app.loader import Document


class RecursiveCharacterTextSplitter:
    """Recursively splits text on natural boundaries (paragraphs, newlines, spaces)."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: List[str] | None = None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "? ", "! ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        """Split a single text string into overlapping chunks."""
        text = text.strip()
        if len(text) <= self.chunk_size:
            return [text] if text else []

        # Find best separator present in the text
        separator = self.separators[-1]
        for sep in self.separators:
            if sep == "" or sep in text:
                separator = sep
                break

        splits = text.split(separator) if separator else list(text)

        chunks: List[str] = []
        current_chunk = ""

        for split in splits:
            piece = split + (separator if separator else "")
            if len(current_chunk) + len(piece) <= self.chunk_size:
                current_chunk += piece
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                # Apply overlap from previous chunk
                overlap_text = current_chunk[-self.chunk_overlap :] if self.chunk_overlap > 0 else ""
                current_chunk = overlap_text + piece

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split a list of Document objects, preserving and augmenting metadata."""
        chunked_docs: List[Document] = []
        for doc_idx, doc in enumerate(documents):
            raw_chunks = self.split_text(doc.text)
            for chunk_idx, chunk in enumerate(raw_chunks):
                chunk_meta = dict(doc.metadata)
                chunk_meta.update(
                    {
                        "chunk_id": f"doc_{doc_idx}_chunk_{chunk_idx}",
                        "chunk_index": chunk_idx,
                        "total_chunks_in_doc": len(raw_chunks),
                    }
                )
                chunked_docs.append(Document(text=chunk, metadata=chunk_meta))
        return chunked_docs
