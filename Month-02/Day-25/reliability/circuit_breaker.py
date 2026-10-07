"""Three-State Circuit Breaker Pattern (CLOSED, OPEN, HALF_OPEN)."""
import time
from enum import Enum
from typing import Callable, Any, Optional


class CircuitState(Enum):
    CLOSED = "CLOSED"         # Normal operation, passes traffic
    OPEN = "OPEN"             # Failing, immediately rejects calls
    HALF_OPEN = "HALF_OPEN"   # Probing downstream health with canary requests


class CircuitBreakerOpenException(Exception):
    """Raised when request is rejected due to active tripped circuit."""
    pass


class CircuitBreaker:
    """Protects downstream LLM endpoints from cascading failures."""

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_time_sec: float = 2.0,
        half_open_successes: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.half_open_successes = half_open_successes

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        now = time.perf_counter()

        # Check transition from OPEN to HALF_OPEN
        if self.state == CircuitState.OPEN:
            if now - self.last_failure_time >= self.recovery_time_sec:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitBreakerOpenException(
                    f"Circuit breaker is OPEN. Fast-failing downstream call."
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_successes:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.perf_counter()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
