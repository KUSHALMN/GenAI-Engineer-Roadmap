from loader import load_pdf
from splitter import split_by_words
from vector_store import add_chunks
from chain import run_chain
from config import PDF_PATH, CHUNK_SIZE, OVERLAP

def ingest(pdf_path: str = PDF_PATH):
    print(f"📄 Ingesting: {pdf_path}")
    text = load_pdf(pdf_path)
    chunks = split_by_words(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP)
    add_chunks(chunks)
    print(f"✅ Done — {len(chunks)} chunks indexed.")

def query(question: str) -> str:
    return run_chain(question)["answer"]

def query_with_context(question: str) -> dict:
    return run_chain(question)
