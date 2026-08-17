from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "llama-3.3-70b-versatile")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    TOP_K: int = int(os.getenv("TOP_K", "4"))
    DEFAULT_RETRIEVER: str = os.getenv("DEFAULT_RETRIEVER", "hybrid")
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", "./data"))

    def ensure_dirs(self) -> None:
        """Ensure necessary directories exist."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
