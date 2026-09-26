"""
Transparent caching wrapper around LLM API calls.
Intercepts calls, checks LLMCache, calls backend on miss, and records metrics.
"""

import time
from typing import Any, Callable, Dict, List, Optional, Union
from llm_cache import LLMCache


class CachedLLMClient:
    """
    Wraps an LLM caller with caching logic, latency benchmarking, and hit telemetry.
    """

    def __init__(
        self,
        llm_caller: Optional[Callable[..., Dict[str, Any]]] = None,
        default_ttl: float = 3600.0,
        enable_cache: bool = True,
    ):
        self.llm_caller = llm_caller or self._default_mock_llm
        self.cache = LLMCache(default_ttl_seconds=default_ttl)
        self.enable_cache = enable_cache

    def _default_mock_llm(
        self, prompt: Union[str, List[Dict[str, str]]], model: str, temperature: float = 0.0, **kwargs
    ) -> Dict[str, Any]:
        """Fallback mock LLM for local benchmarking and offline execution."""
        time.sleep(0.35)  # Simulate network + inference latency
        query_text = prompt if isinstance(prompt, str) else prompt[-1].get("content", "")
        response_text = f"Mock response for: '{query_text}' using model {model}"
        token_count = len(query_text.split()) + 30
        return {
            "choices": [{"message": {"role": "assistant", "content": response_text}}],
            "usage": {
                "prompt_tokens": len(query_text.split()),
                "completion_tokens": 30,
                "total_tokens": token_count,
            },
            "model": model,
        }

    def generate(
        self,
        prompt_or_messages: Union[str, List[Dict[str, str]]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        top_p: float = 1.0,
        bypass_cache: bool = False,
        ttl_seconds: Optional[float] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Execute completion with transparent caching.
        Returns response dict with '_cached': bool metadata.
        """
        # Temperature > 0 usually introduces randomness; by default caching is most suitable for deterministic queries (temp <= 0.2)
        should_cache = self.enable_cache and not bypass_cache

        cache_key = self.cache.generate_cache_key(
            prompt_or_messages=prompt_or_messages,
            model=model,
            temperature=temperature,
            top_p=top_p,
            extra_params=kwargs if kwargs else None,
        )

        if should_cache:
            start_lookup = time.perf_counter()
            cached_result = self.cache.get(cache_key, model=model)
            if cached_result is not None:
                cached_copy = dict(cached_result)
                cached_copy["_cached"] = True
                cached_copy["_cache_lookup_latency_ms"] = round((time.perf_counter() - start_lookup) * 1000, 3)
                return cached_copy

        # Cache miss or bypass: invoke upstream LLM
        start_call = time.perf_counter()
        response = self.llm_caller(
            prompt=prompt_or_messages,
            model=model,
            temperature=temperature,
            top_p=top_p,
            **kwargs,
        )
        call_latency = time.perf_counter() - start_call

        response["latency_seconds"] = call_latency
        response["_cached"] = False

        if should_cache:
            self.cache.put(cache_key, response, ttl_seconds=ttl_seconds)

        return response

    def get_metrics(self) -> Dict[str, Any]:
        """Return cache hit/miss and cost metrics."""
        return self.cache.get_metrics()


if __name__ == "__main__":
    client = CachedLLMClient()

    # Call 1: Miss
    t0 = time.perf_counter()
    r1 = client.generate("Explain vector indexing in databases", model="gpt-4o-mini")
    lat1 = time.perf_counter() - t0
    assert r1["_cached"] is False
    print(f"Call 1 (Miss): Latency={lat1*1000:.1f}ms")

    # Call 2: Hit
    t0 = time.perf_counter()
    r2 = client.generate("Explain vector indexing in databases", model="gpt-4o-mini")
    lat2 = time.perf_counter() - t0
    assert r2["_cached"] is True
    print(f"Call 2 (Hit): Latency={lat2*1000:.1f}ms, Speedup={lat1/max(lat2, 0.0001):.1f}x")

    print("Metrics:", client.get_metrics())
