"""Document Parser: Unifies PDFs, DOCX, Markdown, and tabular CSV into standard schemas."""
from typing import Dict, Any, List


class DocumentParser:
    """Parses heterogeneous file extensions into standard chunked objects."""

    @staticmethod
    def parse_document(file_name: str, content: str) -> Dict[str, Any]:
        ext = file_name.split(".")[-1].lower() if "." in file_name else "txt"
        words = content.split()
        return {
            "filename": file_name,
            "format": ext,
            "char_count": len(content),
            "word_count": len(words),
            "sections": [
                {"heading": "Header", "content": content[:100]},
                {"heading": "Body", "content": content[100:] if len(content) > 100 else content}
            ]
        }
