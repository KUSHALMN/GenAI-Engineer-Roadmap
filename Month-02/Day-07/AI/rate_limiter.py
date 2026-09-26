"""
Thread-Safe Token Bucket Rate Limiter.
Ensures compliance with upstream LLM API RPM (Requests Per Minute) and TPM (Tokens Per Minute).
"""

import threading
import time
from typing import Optional


class TokenBucketRateLimiter:
    """
    Token Bucket Rate Limiter.
    Tokens refill smoothly over time up to capacity.
    """

    def __init__(self, capacity: float, refill_rate_per_second: float):
        if capacity <= 0 or refill_rate_per_second <= 0:
            raise ValueError("Capacity and refill rate must be positive")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate_per_second)
        self.tokens = float(capacity)
        self.last_refill_timestamp = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        """Add tokens earned based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill_timestamp
        self.last_refill_timestamp = now

        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)

    def try_acquire(self, tokens: float = 1.0) -> bool:
        """Non-blocking attempt to acquire tokens. Returns True if successful."""
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def acquire(self, tokens: float = 1.0, timeout: Optional[float] = None) -> bool:
        """
        Blocking acquisition of tokens. Waits until tokens are available or timeout expires.
        """
        start_time = time.monotonic()

        while True:
            with self._lock:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True

                # Calculate sleep duration needed for remaining tokens
                needed = tokens - self.tokens
                wait_time = needed / self.refill_rate

            if timeout is not None:
                elapsed = time.monotonic() - start_time
                if elapsed + wait_time > timeout:
                    return False

            sleep_duration = min(wait_time, 0.05)
            time.sleep(sleep_duration)


if __name__ == "__main__":
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_second=10)

    # First 2 acquire immediately
    assert limiter.try_acquire(1) is True
    assert limiter.try_acquire(1) is True
    # Third fails immediately
    assert limiter.try_acquire(1) is False

    # Blocking acquire with refill
    assert limiter.acquire(1, timeout=0.3) is True
    print("Rate limiter tests passed successfully!")
