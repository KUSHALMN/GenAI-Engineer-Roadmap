"""
app/config.py — Configuration for Day-23 CRAG Service
"""
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Corrective RAG (CRAG) & Self-RAG Guardrail API"
    version: str = "1.0.0"
    upper_confidence_threshold: float = 0.35
    lower_confidence_threshold: float = 0.15
    support_threshold: float = 0.50


settings = Settings()
