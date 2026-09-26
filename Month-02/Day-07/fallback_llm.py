"""
Multi-Provider LLM Fallback Mechanism.
Gracefully cascades through prioritized providers on timeouts, rate-limits, or outages.
"""

from typing import Any, Callable, Dict, List, Optional


class ProviderCallError(Exception):
    pass


class FallbackLLMClient:
    """
    Tries primary provider, falls back to secondary, and terminates at final fallback.
    """

    def __init__(self, providers: Optional[List[Dict[str, Any]]] = None):
        self.providers = providers or self._default_mock_providers()

    def _default_mock_providers(self) -> List[Dict[str, Any]]:
        """Mock providers simulating primary failure and secondary success."""
        def primary_fail(prompt: str, **kwargs):
            raise ProviderCallError("Primary provider (OpenAI) rate limit 429")

        def secondary_succeed(prompt: str, **kwargs):
            return {
                "text": f"Secondary provider (Anthropic) response for: {prompt[:30]}",
                "provider": "Anthropic",
                "model": "claude-3-5-sonnet",
            }

        def tertiary_fallback(prompt: str, **kwargs):
            return {
                "text": f"Tertiary local backup response for: {prompt[:30]}",
                "provider": "LocalOllama",
                "model": "llama3.1:8b",
            }

        return [
            {"name": "OpenAI", "caller": primary_fail},
            {"name": "Anthropic", "caller": secondary_succeed},
            {"name": "LocalOllama", "caller": tertiary_fallback},
        ]

    def call_with_fallback(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Iterate through providers in order until one succeeds."""
        attempt_history: List[Dict[str, str]] = []

        for provider in self.providers:
            name = provider["name"]
            caller = provider["caller"]

            try:
                result = caller(prompt, **kwargs)
                result["_fallback_history"] = attempt_history
                result["_succeeded_provider"] = name
                return result
            except Exception as e:
                attempt_history.append({"provider": name, "error": str(e)})

        raise ProviderCallError(f"All providers exhausted. Attempts: {attempt_history}")


if __name__ == "__main__":
    client = FallbackLLMClient()
    res = client.call_with_fallback("Analyze market trends")
    print("Fallback Result:", res)
    assert res["_succeeded_provider"] == "Anthropic"
    assert len(res["_fallback_history"]) == 1
    assert res["_fallback_history"][0]["provider"] == "OpenAI"
    print("Fallback LLM tests passed successfully!")
