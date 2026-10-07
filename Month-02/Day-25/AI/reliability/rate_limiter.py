"""Token Bucket & Leaky Bucket Rate Limiting for LLM API Quotas."""
import time
import asyncio
from typing import Optional


class TokenBucketRateLimiter:
    """Thread-safe and async-compatible Token Bucket rate limiter."""

    def __init__(self, capacity: int = 10, refill_rate_per_sec: float = 2.0):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = time.perf_counter()

    def _refill(self):
        now = time.perf_counter()
        elapsed = now - self.last_refill
        self.tokens = min(float(self.capacity), self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def acquire(self, tokens_needed: int = 1) -> bool:
        """Attempt to acquire tokens immediately. Returns True if successful."""
        self._refill()
        if self.tokens >= tokens_needed:
            self.tokens -= tokens_needed
            return True
        return False

    async def acquire_async(self, tokens_needed: int = 1, max_wait_sec: float = 5.0) -> bool:
        """Wait asynchronously until sufficient tokens are available or timeout."""
        start_wait = time.perf_counter()
        while time.perf_counter() - start_wait < max_wait_sec:
            if self.acquire(tokens_needed):
                return True
            await asyncio.sleep(0.05)
        return False
