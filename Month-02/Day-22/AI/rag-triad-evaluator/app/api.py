"""
app/api.py — Enterprise FastAPI Service for RAG Triad & Hallucination Assessment
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from core.triad_metrics import compute_rag_triad
from core.hallucination_detector import HallucinationDetector
from core.llm_judge import llm_rag_triad_judge
from app.config import settings

app = FastAPI(
    title="RAG Triad & Hallucination Evaluation Service",
    version=settings.version,
    description="Enterprise API evaluating Context Relevance, Faithfulness, and Factuality in RAG."
)

detector = HallucinationDetector()


class TriadEvalRequest(BaseModel):
    question: str = Field(..., example="What is hybrid search in RAG?")
    context: str = Field(..., example="Hybrid search combines dense vector search with sparse BM25 keyword search.")
    answer: str = Field(..., example="Hybrid search merges dense vector search with BM25 keyword search using RRF.")
    run_llm_judge: bool = Field(default=False)


class TriadEvalResponse(BaseModel):
    question: str
    triad_scores: Dict[str, Any]
    hallucination_analysis: Dict[str, Any]
    judge_scores: Optional[Dict[str, Any]] = None
    passed: bool


@app.get("/health", tags=["Monitoring"])
def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
    }


@app.post("/api/v1/evaluate/rag", response_model=TriadEvalResponse, tags=["Evaluation"])
def evaluate_rag(req: TriadEvalRequest):
    triad = compute_rag_triad(req.question, req.context, req.answer)
    hallucination = detector.evaluate(req.answer, req.context)
    judge = None

    if req.run_llm_judge:
        judge = llm_rag_triad_judge(req.question, req.context, req.answer)

    passed = (
        triad["composite_score"] >= settings.min_composite_score and
        hallucination["hallucination_score"] <= settings.max_hallucination_rate
    )

    return TriadEvalResponse(
        question=req.question,
        triad_scores=triad,
        hallucination_analysis={
            "hallucination_score": hallucination["hallucination_score"],
            "is_safe": hallucination["is_safe"],
            "ungrounded_sentences": hallucination["ungrounded_sentences"],
            "breakdown": hallucination["breakdown"],
        },
        judge_scores=judge,
        passed=passed,
    )
