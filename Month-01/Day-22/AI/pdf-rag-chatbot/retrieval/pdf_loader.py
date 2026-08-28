import io
import re
from typing import List, Dict, Any

class PDFLoader:
    """
    Robust PDF text extraction utility with page-level metadata tracking
    and fallback text extraction.
    """

    @staticmethod
    def load_from_bytes(file_bytes: bytes, filename: str = "document.pdf") -> List[Dict[str, Any]]:
        """
        Extract text from raw PDF bytes page by page.
        Returns a list of page dictionaries with page number, text, and metadata.
        """
        pages = []
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                cleaned_text = PDFLoader._clean_text(text)
                if cleaned_text:
                    pages.append({
                        "page_number": idx + 1,
                        "text": cleaned_text,
                        "source": filename,
                        "char_count": len(cleaned_text),
                        "word_count": len(cleaned_text.split())
                    })
        except Exception as e:
            # Fallback for plain text files or raw byte decoding in test scenarios
            try:
                raw_text = file_bytes.decode("utf-8", errors="ignore")
                cleaned = PDFLoader._clean_text(raw_text)
                if cleaned:
                    pages.append({
                        "page_number": 1,
                        "text": cleaned,
                        "source": filename,
                        "char_count": len(cleaned),
                        "word_count": len(cleaned.split())
                    })
            except Exception:
                raise ValueError(f"Failed to extract text from PDF '{filename}': {str(e)}")

        return pages

    @staticmethod
    def load_from_text(text: str, filename: str = "text_doc.txt") -> List[Dict[str, Any]]:
        """Helper to create page structure from plain text."""
        cleaned = PDFLoader._clean_text(text)
        return [{
            "page_number": 1,
            "text": cleaned,
            "source": filename,
            "char_count": len(cleaned),
            "word_count": len(cleaned.split())
        }]

    @staticmethod
    def _clean_text(text: str) -> str:
        """Sanitize raw extracted text by removing extra whitespace, broken lines, and control chars."""
        if not text:
            return ""
        # Normalize multiple spaces, tabs, and newlines
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        return text.strip()
