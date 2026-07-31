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

if __name__ == "__main__":
    # Test with a sample PDF
    import os
    if os.path.exists("sample.pdf"):
        text = load_pdf("sample.pdf")
        print(f"Extracted {len(text)} characters")
        print(text[:300])
    else:
        print("Place a sample.pdf in this directory to test.")
