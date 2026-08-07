import re
from config import CHUNK_SIZE, OVERLAP

def split_by_words(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def split_by_sentences(text: str, sentences_per_chunk: int = 5) -> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def split_by_paragraphs(text: str) -> list[str]:
    paragraphs = re.split(r'\n{2,}', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]
