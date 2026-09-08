from fastapi import FastAPI
from pydantic import BaseModel, Field

try:
    from .rag_pipeline import OptimizedRAGPipeline
except ImportError:
    from rag_pipeline import OptimizedRAGPipeline

app = FastAPI(title="Optimized RAG Service - Day 29")
pipeline = OptimizedRAGPipeline()

class RAGQuery(BaseModel):
    query: str = Field(..., min_length=1)

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 29: Production RAG Optimization"}

@app.post("/api/v1/rag/query")
def execute_rag(req: RAGQuery):
    return pipeline.query(req.query)
