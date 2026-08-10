import fitz  # PyMuPDF
from config import CHUNK_SIZE, CHUNK_OVERLAP


def load_pdf(path: str) -> str:
    doc = fitz.open(path)
    return " ".join(page.get_text() for page in doc)


def chunk_text(text: str) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def load_and_chunk(path: str) -> list[str]:
    return chunk_text(load_pdf(path))
