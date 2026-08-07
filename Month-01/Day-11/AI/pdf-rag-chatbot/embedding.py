from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def embed_texts(texts: list[str]) -> list[list[float]]:
    return get_model().encode(texts).tolist()

def embed_query(query: str) -> list[float]:
    return get_model().encode(query).tolist()
