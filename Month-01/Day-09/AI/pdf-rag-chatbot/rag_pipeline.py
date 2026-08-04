import os
from groq import Groq
from dotenv import load_dotenv
from pdf_loader import load_pdf
from chunking import chunk_by_words
from vector_store import add_chunks
from retriever import retrieve
from prompt_builder import build_prompt

load_dotenv()
_client = None

def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client

def ingest(pdf_path: str, chunk_size: int = 200, overlap: int = 30):
    """Load PDF, chunk, embed and store in vector DB."""
    print(f"📄 Ingesting: {pdf_path}")
    text = load_pdf(pdf_path)
    chunks = chunk_by_words(text, chunk_size=chunk_size, overlap=overlap)
    add_chunks(chunks)
    print(f"✅ Ingestion complete — {len(chunks)} chunks indexed.")

def query(question: str, n_results: int = 3) -> str:
    """Retrieve context and generate answer using LLM."""
    context_chunks = retrieve(question, n_results=n_results)
    messages = build_prompt(question, context_chunks)
    response = get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return response.choices[0].message.content
