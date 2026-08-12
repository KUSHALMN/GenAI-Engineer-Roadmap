import fitz  # PyMuPDF


def load_pdf(path: str) -> str:
    doc = fitz.open(path)
    return " ".join(page.get_text() for page in doc)
