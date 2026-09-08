from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Any

try:
    from .rag_pipeline import OptimizedRAGPipeline
except ImportError:
    from rag_pipeline import OptimizedRAGPipeline

app = FastAPI(
    title="Production RAG Optimization Service",
    description="Optimized RAG with Cross-Encoder reranking, semantic caching, and citations.",
    version="1.0.0"
)

pipeline = OptimizedRAGPipeline()

class RAGQuery(BaseModel):
    query: str = Field(..., min_length=1)

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 29: Production RAG Optimization"}

@app.post("/api/v1/rag/query")
def execute_rag(req: RAGQuery):
    return pipeline.query(req.query)

@app.post("/api/v1/rag/cache/clear")
def clear_cache():
    pipeline.cache.clear()
    return {"status": "cache_cleared"}
