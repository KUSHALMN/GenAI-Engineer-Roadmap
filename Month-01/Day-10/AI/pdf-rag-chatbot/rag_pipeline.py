from loader import load_pdf
from splitter import split_by_words
from vector_store import add_chunks
from chain import run_chain

def ingest(pdf_path: str, chunk_size: int = 200, overlap: int = 30):
    """Load PDF → split → embed → store in ChromaDB."""
    print(f"📄 Ingesting: {pdf_path}")
    text = load_pdf(pdf_path)
    chunks = split_by_words(text, chunk_size=chunk_size, overlap=overlap)
    add_chunks(chunks)
    print(f"✅ Ingestion complete — {len(chunks)} chunks indexed.")

def query(question: str, n_results: int = 3) -> str:
    """Run full RAG chain and return answer."""
    result = run_chain(question, n_results=n_results)
    return result["answer"]

def query_with_context(question: str, n_results: int = 3) -> dict:
    """Run full RAG chain and return answer + context."""
    return run_chain(question, n_results=n_results)
