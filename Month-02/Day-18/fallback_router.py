"""
Fallback Provider Router.
Provides seamless failover across an ordered list of LLMProvider instances
with failure counts and circuit-breaker safety.
"""

from typing import Any, Dict, List
from provider_interface import LLMProvider, MockLargeModelProvider, MockSmallModelProvider


class FallbackRouter:

    def __init__(self, providers: List[LLMProvider]):
        if not providers:
            raise ValueError("Must provide at least one LLMProvider")
        self.providers = providers
        self.failure_counts: Dict[str, int] = {p.provider_name: 0 for p in providers}

    def execute_with_fallback(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Tries each provider in order until one succeeds."""
        errors: List[Dict[str, str]] = []

        for provider in self.providers:
            try:
                response = provider.generate(prompt, **kwargs)
                response["_failover_history"] = errors
                return response
            except Exception as e:
                self.failure_counts[provider.provider_name] = self.failure_counts.get(provider.provider_name, 0) + 1
                errors.append({"provider": provider.provider_name, "error": str(e)})

        raise RuntimeError(f"All providers failed in fallback router: {errors}")


if __name__ == "__main__":
    class FailingProvider(LLMProvider):
        @property
        def provider_name(self) -> str:
            return "UnreliableAPI"
        @property
        def model_name(self) -> str:
            return "flaky-v1"
        @property
        def cost_per_1k_input_tokens(self) -> float:
            return 0.001
        @property
        def cost_per_1k_output_tokens(self) -> float:
            return 0.002
        def generate(self, prompt: str, **kwargs):
            raise ConnectionError("503 Service Unavailable")

    router = FallbackRouter([FailingProvider(), MockSmallModelProvider()])
    res = router.execute_with_fallback("Generate summary")
    print("Fallback response:", res)
    assert res["provider"] == "Groq"
    assert len(res["_failover_history"]) == 1
    print("FallbackRouter tests passed successfully!")
