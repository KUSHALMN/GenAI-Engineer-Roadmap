"""
Unified LLM Provider Interface.
Abstract Base Class establishing standard data contracts across diverse model backends
(OpenAI, Anthropic, Groq, Ollama, HuggingFace).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMProvider(ABC):
    """Abstract interface for LLM provider implementations."""

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.0, max_tokens: int = 512, **kwargs) -> Dict[str, Any]:
        """Generate text completion from prompt."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of provider (e.g., 'OpenAI', 'Anthropic', 'Groq')."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Model identifier (e.g., 'gpt-4o-mini', 'claude-3-5-sonnet')."""
        pass

    @property
    @abstractmethod
    def cost_per_1k_input_tokens(self) -> float:
        """Input token pricing."""
        pass

    @property
    @abstractmethod
    def cost_per_1k_output_tokens(self) -> float:
        """Output token pricing."""
        pass


class MockSmallModelProvider(LLMProvider):
    """Fast, cheap model for extraction, classification, and short queries."""

    @property
    def provider_name(self) -> str:
        return "Groq"

    @property
    def model_name(self) -> str:
        return "llama-3-8b-instant"

    @property
    def cost_per_1k_input_tokens(self) -> float:
        return 0.00008

    @property
    def cost_per_1k_output_tokens(self) -> float:
        return 0.00008

    def generate(self, prompt: str, temperature: float = 0.0, max_tokens: int = 512, **kwargs) -> Dict[str, Any]:
        return {
            "text": f"[SmallModel-8B]: Fast response to '{prompt[:35]}...'",
            "provider": self.provider_name,
            "model": self.model_name,
            "usage": {"prompt_tokens": len(prompt.split()), "completion_tokens": 15},
        }


class MockLargeModelProvider(LLMProvider):
    """Frontier model for complex reasoning, code generation, and multi-step math."""

    @property
    def provider_name(self) -> str:
        return "Anthropic"

    @property
    def model_name(self) -> str:
        return "claude-3-5-sonnet"

    @property
    def cost_per_1k_input_tokens(self) -> float:
        return 0.003

    @property
    def cost_per_1k_output_tokens(self) -> float:
        return 0.015

    def generate(self, prompt: str, temperature: float = 0.0, max_tokens: int = 512, **kwargs) -> Dict[str, Any]:
        return {
            "text": f"[LargeModel-Sonnet]: In-depth reasoning and analysis for '{prompt[:35]}...'",
            "provider": self.provider_name,
            "model": self.model_name,
            "usage": {"prompt_tokens": len(prompt.split()), "completion_tokens": 60},
        }


if __name__ == "__main__":
    small = MockSmallModelProvider()
    large = MockLargeModelProvider()
    assert small.cost_per_1k_input_tokens < large.cost_per_1k_input_tokens
    print("Provider interface tests passed successfully!")
