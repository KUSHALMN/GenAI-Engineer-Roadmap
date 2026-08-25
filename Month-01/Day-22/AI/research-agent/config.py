"""
Configuration Module for StateGraph Research Agent with Checkpoint Memory
Handles environment variables, API credentials, memory persistence settings,
and execution runtime parameters.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AgentConfig:
    """Central configuration for Research Agent State Graph & Memory execution."""
    
    # Provider Settings
    groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Model Selection
    default_groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    default_openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Agent Hyperparameters
    temperature: float = 0.1
    max_tokens: int = 2048
    max_steps: int = 8
    max_search_results: int = 3
    
    # Memory & Checkpoint Settings
    checkpoint_dir: str = os.getenv("CHECKPOINT_DIR", ".checkpoints")
    max_history_turns: int = 10
    enable_memory_persistence: bool = True
    
    # Offline Simulation Mode
    simulation_mode: bool = False

    def __post_init__(self):
        if not self.groq_api_key and not self.openai_api_key:
            self.simulation_mode = True


# Global default configuration instance
config = AgentConfig()
