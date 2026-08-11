import chromadb
from app.config import CHROMA_DIR, COLLECTION_NAME

_collection = None


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def upsert(chunks: list[str], embeddings: list):
    col = get_collection()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    col.upsert(documents=chunks, embeddings=embeddings, ids=ids)


def query(embedding: list, n: int) -> list[str]:
    col = get_collection()
    results = col.query(query_embeddings=[embedding], n_results=n)
    return results["documents"][0]
