"""
app/config.py — Configuration for RAG Triad Evaluator
"""
import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "RAG Triad Evaluator & Hallucination Guardrail"
    version: str = "1.0.0"
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    default_model: str = "llama3-8b-8192"
    min_composite_score: float = 0.50
    max_hallucination_rate: float = 0.25


settings = Settings()
