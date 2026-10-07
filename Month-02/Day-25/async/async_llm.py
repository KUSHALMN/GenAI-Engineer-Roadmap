"""High-throughput Asynchronous LLM Client with Circuit Breakers & Rate Limiting."""
import sys
import os
import asyncio
from typing import List, Dict, Any, Optional

# Ensure Day-25 root is on python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reliability.rate_limiter import TokenBucketRateLimiter
from reliability.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException
from reliability.backoff import ExponentialBackoff


class AsyncResilientLLM:
    """Production asynchronous LLM client managing rate limits, retries, and circuit breaking."""

    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.rate_limiter = TokenBucketRateLimiter(capacity=5, refill_rate_per_sec=5.0)
        self.circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_time_sec=1.5)
        self.backoff = ExponentialBackoff(base_delay=0.1, max_delay=1.0)

    async def _mock_raw_call(self, prompt: str, fail_prob: float = 0.0) -> str:
        """Simulate async network call with simulated latency."""
        await asyncio.sleep(0.05)
        if fail_prob > 0.0:
            import random
            if random.random() < fail_prob:
                raise ConnectionError("Simulated LLM upstream 503 Service Unavailable")
        return f"[{self.model_name}] Response to '{prompt}'"

    async def generate(self, prompt: str, max_retries: int = 2) -> Dict[str, Any]:
        """Execute resilient async call."""
        # 1. Rate limiter check
        acquired = await self.rate_limiter.acquire_async(tokens_needed=1, max_wait_sec=2.0)
        if not acquired:
            return {"status": "RATE_LIMITED", "error": "Rate limit quota exceeded"}

        # 2. Resilient invocation with circuit breaker & retry
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                # Wrap through circuit breaker
                def cb_invocation():
                    # For sync wrapper compatibility in our circuit breaker
                    loop = asyncio.get_event_loop()
                    return loop.run_until_complete(self._mock_raw_call(prompt))

                # Direct async invocation with circuit breaker state check
                if self.circuit_breaker.state.value == "OPEN":
                    raise CircuitBreakerOpenException("Circuit open: fast-failing")

                output = await self._mock_raw_call(prompt)
                self.circuit_breaker._on_success()
                return {"status": "SUCCESS", "response": output, "attempts": attempt + 1}
            except Exception as e:
                self.circuit_breaker._on_failure()
                last_error = str(e)
                if attempt < max_retries:
                    delay = self.backoff.compute_delay(attempt)
                    await asyncio.sleep(delay)

        return {"status": "FAILED", "error": last_error, "attempts": max_retries + 1}

    async def batch_generate(self, prompts: List[str]) -> List[Dict[str, Any]]:
        """Run multiple requests concurrently using asyncio.gather."""
        tasks = [self.generate(p) for p in prompts]
        return await asyncio.gather(*tasks)


async def main():
    llm = AsyncResilientLLM()
    prompts = [
        "What is gradient descent?",
        "Explain backpropagation.",
        "How do transformers use self-attention?",
        "Explain LoRA fine-tuning."
    ]
    print("Executing async concurrent batch generation...")
    results = await llm.batch_generate(prompts)
    for p, res in zip(prompts, results):
        print(f"Prompt: '{p[:25]}...' -> {res['status']} ({res.get('response', res.get('error'))})")


if __name__ == "__main__":
    asyncio.run(main())
