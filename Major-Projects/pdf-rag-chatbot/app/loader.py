from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List


class Document:
    """Represents a loaded document chunk with text and metadata."""

    def __init__(self, text: str, metadata: Dict[str, Any] | None = None):
        self.text = text
        self.metadata = metadata or {}

    def __repr__(self) -> str:
        return f"Document(metadata={self.metadata}, text_snippet={self.text[:50]!r}...)"


def load_pdf(file_path: str | Path) -> List[Document]:
    """Load text and page metadata from a PDF file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    documents: List[Document] = []
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        for page_idx, page in enumerate(reader.pages, start=1):
            extracted = page.extract_text() or ""
            cleaned = extracted.strip()
            if cleaned:
                documents.append(
                    Document(
                        text=cleaned,
                        metadata={
                            "source": path.name,
                            "page": page_idx,
                            "total_pages": len(reader.pages),
                        },
                    )
                )
    except ImportError:
        # Fallback reading raw text if pypdf is not installed
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            if text.strip():
                documents.append(
                    Document(
                        text=text.strip(),
                        metadata={"source": path.name, "page": 1, "total_pages": 1},
                    )
                )

    return documents


def load_text_file(file_path: str | Path) -> List[Document]:
    """Load a plain text or markdown file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    return [
        Document(
            text=text.strip(),
            metadata={"source": path.name, "page": 1, "total_pages": 1},
        )
    ]
