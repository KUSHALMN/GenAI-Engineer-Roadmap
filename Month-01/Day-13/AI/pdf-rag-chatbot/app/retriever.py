from app.embedding import embed
from app.vector_store import upsert, query
from app.config import TOP_K


def store(chunks: list[str]):
    embeddings = embed(chunks)
    upsert(chunks, embeddings)


def retrieve(question: str) -> list[str]:
    embedding = embed([question])[0]
    return query(embedding, TOP_K)
