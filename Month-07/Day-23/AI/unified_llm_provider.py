"""
LLM Provider Abstraction: Unified Provider Interface, Normalized Token Usages,
Automatic Fallback Cascades, and Standardized Error Envelopes.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class NormalizedInferenceResult:
    provider: str
    model: str
    text: str
    prompt_tokens: int
    completion_tokens: int
    finish_reason: str


class UnifiedLLMProviderAdapter:
    def __init__(self):
        self.providers: Dict[str, str] = {
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-5-haiku",
            "local_vllm": "llama-3-8b-instruct"
        }

    def complete(self, prompt: str, primary_provider: str = "openai") -> NormalizedInferenceResult:
        cascade_order = [primary_provider, "anthropic", "local_vllm"]
        for p in cascade_order:
            try:
                # Simulated dispatch
                return NormalizedInferenceResult(
                    provider=p,
                    model=self.providers[p],
                    text=f"Response from {p} for prompt: {prompt[:15]}...",
                    prompt_tokens=len(prompt.split()),
                    completion_tokens=25,
                    finish_reason="stop"
                )
            except Exception:
                continue
        raise RuntimeError("All LLM providers in cascade failed!")


if __name__ == "__main__":
    adapter = UnifiedLLMProviderAdapter()
    res = adapter.complete("Explain Kubernetes Pod scheduling in 2 sentences.")
    assert res.provider == "openai"
    assert res.completion_tokens == 25
    print("=== Day 23: Unified LLM Provider Adapter ===")
    print(f"Provider: {res.provider} | Model: {res.model} | Tokens: {res.prompt_tokens + res.completion_tokens}")
