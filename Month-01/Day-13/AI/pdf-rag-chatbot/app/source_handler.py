from app.loader import load_pdf
from app.splitter import split_text


def load_and_chunk(path: str) -> list[str]:
    text = load_pdf(path)
    return split_text(text)
