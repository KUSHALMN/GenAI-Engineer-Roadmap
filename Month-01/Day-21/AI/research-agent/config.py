"""
Configuration Module for StateGraph Research Agent
Handles environment variable loading, API credentials, model parameters,
and execution runtime settings.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load .env file from project root or current working directory
load_dotenv()


@dataclass
class AgentConfig:
    """Central configuration for Research Agent State Graph execution."""
    
    # Provider Settings
    groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Model Selection (defaults to Groq LLaMA 3.3 70B Versatile or OpenAI GPT-4o-mini)
    default_groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    default_openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Agent Hyperparameters
    temperature: float = 0.1
    max_tokens: int = 2048
    max_steps: int = 8  # Maximum graph cycle loop iterations to avoid infinite loops
    max_search_results: int = 3
    
    # Offline Simulation Mode (Activated automatically if no API keys are found)
    simulation_mode: bool = False

    def __post_init__(self):
        if not self.groq_api_key and not self.openai_api_key:
            self.simulation_mode = True


# Global default configuration instance
config = AgentConfig()
