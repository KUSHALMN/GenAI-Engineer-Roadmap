"""
app/api.py — Enterprise FastAPI Service for Corrective RAG (CRAG) & Self-RAG
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Any

from app.crag_engine import CRAGEngine
from core.self_rag_guardrail import SelfRAGGuardrail
from app.config import settings

app = FastAPI(
    title="Corrective RAG (CRAG) & Self-RAG Microservice",
    version=settings.version,
    description="Production API with retrieval evaluation, knowledge striping, and Self-RAG critique guardrails."
)

engine = CRAGEngine()
guardrail = SelfRAGGuardrail()


class CRAGRequest(BaseModel):
    query: str = Field(..., example="What are the benefits of LoRA fine-tuning?")


class ReflectRequest(BaseModel):
    query: str = Field(..., example="Explain Model Context Protocol.")
    context: str = Field(..., example="Model Context Protocol standardizes AI client-server tool communication.")
    response: str = Field(..., example="MCP standardizes AI tool communication via JSON-RPC.")


@app.get("/health", tags=["Monitoring"])
def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
    }


@app.post("/api/v1/crag/query", tags=["CRAG Pipeline"])
def run_crag_query(req: CRAGRequest):
    return engine.query(req.query)


@app.post("/api/v1/self-rag/reflect", tags=["Guardrails"])
def run_self_reflection(req: ReflectRequest):
    return guardrail.reflect(req.query, req.context, req.response)
