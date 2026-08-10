import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K

_model = None
_collection = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def store_chunks(chunks: list[str]):
    col = _get_collection()
    model = _get_model()
    embeddings = model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    col.upsert(documents=chunks, embeddings=embeddings, ids=ids)


def retrieve(query: str) -> list[str]:
    col = _get_collection()
    model = _get_model()
    embedding = model.encode([query]).tolist()
    results = col.query(query_embeddings=embedding, n_results=TOP_K)
    return results["documents"][0]
