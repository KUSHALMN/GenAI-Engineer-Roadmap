from pypdf import PdfReader

def load_pdf(filepath: str) -> str:
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

def load_pdf_by_pages(filepath: str) -> list[str]:
    reader = PdfReader(filepath)
    return [page.extract_text() or "" for page in reader.pages]
