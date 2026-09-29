"""
app/config.py — Configuration settings for Evaluation Framework
"""
import os
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "LLM Evaluation Framework"
    version: str = "1.0.0"
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    default_judge_model: str = "llama3-8b-8192"
    f1_passing_threshold: float = 0.50
    correctness_passing_threshold: float = 3.5


settings = Settings()
