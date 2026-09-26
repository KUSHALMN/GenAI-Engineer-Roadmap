"""
Resilient LLM Service.
Wires together:
1. Rate Limiting (Token Bucket)
2. Timeout Enforcement
3. Exponential Backoff Retry with Jitter
4. Multi-Provider Fallback Routing
"""

import concurrent.futures
import time
from typing import Any, Dict, List, Optional
from fallback_llm import FallbackLLMClient, ProviderCallError
from rate_limiter import TokenBucketRateLimiter
from retry import exponential_backoff_retry


class ResilientLLMService:

    def __init__(
        self,
        rpm_limit: float = 60.0,
        request_timeout_seconds: float = 5.0,
        max_retries: int = 2,
    ):
        self.rate_limiter = TokenBucketRateLimiter(
            capacity=max(2.0, rpm_limit / 10.0),
            refill_rate_per_second=rpm_limit / 60.0,
        )
        self.fallback_client = FallbackLLMClient()
        self.request_timeout = request_timeout_seconds
        self.max_retries = max_retries

    def _execute_with_timeout(self, func, *args, **kwargs) -> Any:
        """Enforces hard execution timeout."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=self.request_timeout)
            except concurrent.futures.TimeoutError as exc:
                raise TimeoutError(f"Request timed out after {self.request_timeout}s") from exc

    def execute_query(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Executes query through Rate Limiter -> Timeout Handler -> Retry -> Fallback.
        """
        # 1. Rate Limiter Gate
        acquired = self.rate_limiter.acquire(tokens=1.0, timeout=2.0)
        if not acquired:
            raise RuntimeError("Rate limit exceeded: could not acquire token bucket permit")

        # 2. Resilient Execution with Retry
        @exponential_backoff_retry(
            max_retries=self.max_retries,
            base_delay=0.05,
            max_delay=0.5,
            retryable_exceptions=(TimeoutError, ConnectionError),
        )
        def _call_core():
            return self._execute_with_timeout(
                self.fallback_client.call_with_fallback,
                prompt,
                **kwargs,
            )

        start_time = time.perf_counter()
        result = _call_core()
        duration = time.perf_counter() - start_time

        result["_service_latency_ms"] = round(duration * 1000, 2)
        return result


if __name__ == "__main__":
    service = ResilientLLMService(rpm_limit=120.0, request_timeout_seconds=3.0, max_retries=2)
    response = service.execute_query("Generate production deployment checklist")
    print("Resilient Service Response:", response)
    assert response["_succeeded_provider"] == "Anthropic"
    print("Resilient LLM Service passed all tests!")
