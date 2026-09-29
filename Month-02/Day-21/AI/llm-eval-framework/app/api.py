"""
app/api.py — Enterprise FastAPI Service for LLM Evaluation
Endpoints for single evaluation, batch scoring, and health probes.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from core.metrics import compute_lexical_metrics
from core.llm_judge import evaluate_with_llm_judge
from app.config import settings

app = FastAPI(
    title="LLM Evaluation Platform API",
    version=settings.version,
    description="Production-grade API for scoring LLM outputs via Lexical & LLM-as-a-Judge metrics."
)


class EvalRequest(BaseModel):
    question: str = Field(..., example="What is RAG?")
    context: str = Field(..., example="Retrieval-Augmented Generation combines retrieval with generation.")
    expected: str = Field(..., example="RAG combines retrieval with generation.")
    prediction: str = Field(..., example="RAG combines search retrieval with generative LLMs.")
    run_llm_judge: bool = Field(default=False)


class EvalResponse(BaseModel):
    question: str
    prediction: str
    expected: str
    lexical_metrics: Dict[str, Any]
    judge_metrics: Optional[Dict[str, Any]] = None
    passed: bool


class BatchEvalRequest(BaseModel):
    items: List[EvalRequest]


@app.get("/health", tags=["Monitoring"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
    }


@app.post("/api/v1/evaluate/single", response_model=EvalResponse, tags=["Evaluation"])
def evaluate_single(req: EvalRequest):
    lexical = compute_lexical_metrics(req.prediction, req.expected)
    judge = None
    passed = lexical["f1"] >= settings.f1_passing_threshold

    if req.run_llm_judge:
        judge = evaluate_with_llm_judge(req.question, req.context, req.expected, req.prediction)
        if judge.get("correctness", 0) < settings.correctness_passing_threshold:
            passed = False

    return EvalResponse(
        question=req.question,
        prediction=req.prediction,
        expected=req.expected,
        lexical_metrics=lexical,
        judge_metrics=judge,
        passed=passed
    )


@app.post("/api/v1/evaluate/batch", tags=["Evaluation"])
def evaluate_batch(batch: BatchEvalRequest):
    results = [evaluate_single(item) for item in batch.items]
    avg_f1 = sum(r.lexical_metrics["f1"] for r in results) / len(results) if results else 0.0
    pass_rate = sum(1 for r in results if r.passed) / len(results) if results else 0.0

    return {
        "total_evaluated": len(results),
        "mean_f1": round(avg_f1, 4),
        "pass_rate": round(pass_rate, 4),
        "evaluations": results
    }
