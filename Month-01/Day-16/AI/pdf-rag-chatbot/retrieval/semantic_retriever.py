from app.embedding import embed
from app.vector_store import query_vector
from app.config import TOP_K


def semantic_retrieve(question: str) -> list[str]:
    embedding = embed([question])[0]
    return query_vector(embedding, TOP_K)
