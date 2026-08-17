from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.config import settings
from app.rag_pipeline import pipeline

app = FastAPI(
    title="PDF RAG Chatbot API",
    description="Advanced PDF RAG pipeline with Semantic, BM25 Keyword, Hybrid RRF retrieval and Reranking.",
    version="1.0.0",
)


class TextIndexRequest(BaseModel):
    text: str
    source_name: Optional[str] = "manual_text"


class QueryRequest(BaseModel):
    question: str
    retriever_type: Optional[str] = "hybrid"  # semantic | keyword | hybrid
    top_k: Optional[int] = 4
    use_reranker: Optional[bool] = True


class AskSimpleRequest(BaseModel):
    question: str
    context: Optional[str] = ""


@app.get("/health")
def health() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "chat_model": settings.CHAT_MODEL,
        "indexed_chunks": len(pipeline.indexed_documents),
    }


@app.post("/index-text")
def index_text(payload: TextIndexRequest) -> Dict[str, Any]:
    """Index raw text passages directly into the RAG store."""
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    result = pipeline.ingest_raw_text(payload.text, source_name=payload.source_name or "manual_text")
    return {"status": "success", "data": result}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload and ingest a PDF document."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")

    settings.ensure_dirs()
    save_path = settings.DATA_DIR / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = pipeline.ingest_file(save_path)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


@app.post("/query")
def query_rag(payload: QueryRequest) -> Dict[str, Any]:
    """Execute end-to-end RAG query with selected retriever mode and reranker."""
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = pipeline.query(
        question=payload.question,
        retriever_type=payload.retriever_type or "hybrid",
        top_k=payload.top_k or 4,
        use_reranker=payload.use_reranker if payload.use_reranker is not None else True,
    )
    return result


@app.post("/ask")
def ask(payload: AskSimpleRequest) -> Dict[str, str]:
    """Simplified compatibility endpoint."""
    if payload.context:
        pipeline.ingest_raw_text(payload.context, source_name="context_input")
    res = pipeline.query(question=payload.question)
    return {"answer": res["answer"]}


@app.post("/clear")
def clear_indices() -> Dict[str, str]:
    """Clear all vector and keyword indices."""
    pipeline.clear()
    return {"status": "cleared"}


def main() -> None:
    settings.ensure_dirs()
    print("=" * 60)
    print("[*] PDF RAG Chatbot CLI Test")
    print(f"Model: {settings.CHAT_MODEL} | Default Retriever: {settings.DEFAULT_RETRIEVER}")
    print("=" * 60)

    # Ingest a sample text for demonstration
    sample_doc = (
        "Retrieval-Augmented Generation (RAG) optimizes the output of an LLM by referencing an "
        "authoritative knowledge base outside of its training data sources before generating a response. "
        "Hybrid search combines dense vector embeddings with sparse keyword algorithms like BM25 to get the "
        "benefits of both semantic understanding and exact keyword precision. "
        "Reciprocal Rank Fusion (RRF) merges multiple ranking lists using rank inverse scores."
    )
    print("\n[1] Ingesting sample knowledge document...")
    ingest_res = pipeline.ingest_raw_text(sample_doc, source_name="rag_overview_doc")
    print(f"Indexed chunks: {ingest_res['chunks_created']}")

    print("\n[2] Executing Hybrid Search + Reranking Query...")
    sample_query = "How does hybrid search work and what is RRF?"
    answer_res = pipeline.query(sample_query, retriever_type="hybrid", use_reranker=True)

    print(f"\nQuestion: {sample_query}")
    print(f"Answer: {answer_res['answer']}")
    print(f"Retrieved passages count: {answer_res['retrieved_count']}")
    print("Sources:", answer_res["sources"])
    print("\n[+] System test completed successfully.")


if __name__ == "__main__":
    main()
