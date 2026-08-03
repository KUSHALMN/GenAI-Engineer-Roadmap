from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return model.encode(texts).tolist()

def embed_query(query: str) -> list[float]:
    model = get_model()
    return model.encode(query).tolist()
