from app.vector_store import get_all_chunks
from app.config import TOP_K


def keyword_retrieve(question: str) -> list[str]:
    keywords = set(question.lower().split())
    chunks = get_all_chunks()

    scored = []
    for chunk in chunks:
        words = set(chunk.lower().split())
        score = len(keywords & words)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:TOP_K]]
