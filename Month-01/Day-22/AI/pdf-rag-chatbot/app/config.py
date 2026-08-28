import os
from typing import Optional
from pydantic import BaseModel, Field

class Settings(BaseModel):
    """
    Application configuration settings loaded from environment variables with sensible defaults.
    """
    APP_NAME: str = "Enterprise PDF RAG Chatbot"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    
    # LLM Settings
    LLM_PROVIDER: str = Field(default_factory=lambda: os.getenv("LLM_PROVIDER", "mock")) # "groq", "openai", "mock"
    LLM_MODEL: str = Field(default_factory=lambda: os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"))
    OPENAI_API_KEY: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    GROQ_API_KEY: Optional[str] = Field(default_factory=lambda: os.getenv("GROQ_API_KEY"))
    TEMPERATURE: float = 0.2
    MAX_TOKENS: int = 2048
    
    # Embedding & Vector Store Settings
    EMBEDDING_DIMENSION: int = 384
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.35
    
    # Hybrid Retrieval (RRF)
    RRF_K: int = 60
    BM25_WEIGHT: float = 0.4
    DENSE_WEIGHT: float = 0.6
    
    # Streaming Settings
    STREAM_CHUNK_DELAY_MS: int = 15  # Artificial delay for mock stream simulation

settings = Settings()
