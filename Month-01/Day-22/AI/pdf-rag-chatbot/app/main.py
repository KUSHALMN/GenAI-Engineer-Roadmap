import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, status
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import settings
from app.rag_pipeline import RAGPipeline
from app.streaming import StreamingRAGService

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready PDF RAG Chatbot API with Hybrid Retrieval, Citation Sources, and SSE Streaming."
)

# Enable CORS for web frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global singleton RAG pipeline
pipeline = RAGPipeline()


# =============================================================================
# Request & Response Schemas
# =============================================================================
class QueryRequest(BaseModel):
    question: str = Field(..., example="What are the key architectural components described in the document?")
    top_k: Optional[int] = Field(default=4, ge=1, le=20)

class IngestTextRequest(BaseModel):
    title: str = Field(default="document.txt", example="company_policy.txt")
    content: str = Field(..., example="This is document content about generative AI systems...")

class CitationItem(BaseModel):
    source: str
    page: int
    chunk_id: str
    score: float
    snippet: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[CitationItem]
    retrieved_count: int
    latency_ms: float

class IngestResponse(BaseModel):
    message: str
    filename: str
    page_count: int
    chunk_count: int
    indexed_count: int

class StatsResponse(BaseModel):
    total_documents: int
    total_chunks: int
    sources: List[str]
    files: List[Dict[str, Any]]


# =============================================================================
# API Endpoints
# =============================================================================
@app.get("/health", tags=["Health"])
async def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "indexed_chunks": pipeline.vector_store.count(),
        "total_documents": len(pipeline.ingested_files)
    }

@app.post(f"{settings.API_PREFIX}/upload", response_model=IngestResponse, tags=["Ingestion"])
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and index a PDF file for hybrid RAG search.
    """
    if not file.filename.lower().endswith((".pdf", ".txt", ".md")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, TXT, and MD files are supported."
        )

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    try:
        meta = pipeline.ingest_pdf(file_bytes, filename=file.filename)
        return IngestResponse(
            message="Document successfully processed and indexed into vector & keyword stores.",
            filename=meta["filename"],
            page_count=meta["page_count"],
            chunk_count=meta["chunk_count"],
            indexed_count=meta["indexed_count"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

@app.post(f"{settings.API_PREFIX}/ingest-text", response_model=IngestResponse, tags=["Ingestion"])
async def ingest_text(payload: IngestTextRequest):
    """
    Direct text ingestion endpoint for testing and raw text documents.
    """
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")

    meta = pipeline.ingest_text(payload.content, filename=payload.title)
    return IngestResponse(
        message="Text successfully indexed into hybrid retrieval store.",
        filename=meta["filename"],
        page_count=meta["page_count"],
        chunk_count=meta["chunk_count"],
        indexed_count=meta["indexed_count"]
    )

@app.post(f"{settings.API_PREFIX}/query", response_model=QueryResponse, tags=["RAG"])
async def query_rag(payload: QueryRequest):
    """
    Standard synchronous RAG question-answering with citation tracking and hybrid retrieval.
    """
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = pipeline.query(payload.question, top_k=payload.top_k or 4)
    return QueryResponse(**result)

@app.post(f"{settings.API_PREFIX}/query/stream", tags=["Streaming"])
async def stream_rag(payload: QueryRequest):
    """
    Server-Sent Events (SSE) streaming endpoint for real-time token delivery.
    """
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    stream_generator = StreamingRAGService.stream_query(
        pipeline=pipeline,
        query=payload.question,
        top_k=payload.top_k or 4
    )

    return StreamingResponse(
        stream_generator,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.get(f"{settings.API_PREFIX}/documents", response_model=StatsResponse, tags=["Management"])
async def get_documents():
    """List all indexed documents and vector store stats."""
    return pipeline.get_stats()

@app.delete(f"{settings.API_PREFIX}/documents", tags=["Management"])
async def clear_documents():
    """Clear all indexed documents and reset the database."""
    pipeline.clear()
    return {"message": "All indexed documents and vectors have been cleared successfully."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
