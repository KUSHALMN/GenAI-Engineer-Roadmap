from app.loader import load_pdf
from app.splitter import split_text


def load_and_chunk(path: str) -> list[str]:
    return split_text(load_pdf(path))
