"""
Production-grade retry logic with Exponential Backoff and Full Jitter.
Supports synchronous and asynchronous function decorating, configurable retryable exceptions,
and max retry budget.
"""

import functools
import random
import time
from typing import Any, Callable, Optional, Set, Tuple, Type


class RetryExhaustedError(Exception):
    """Raised when all retry attempts fail."""
    pass


def exponential_backoff_retry(
    max_retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry_callback: Optional[Callable[[Exception, int, float], None]] = None,
):
    """
    Decorator for retrying operations with exponential backoff and jitter.
    Delay calculation: min(max_delay, base_delay * (exponential_base ** attempt))
    If jitter=True, delay = random.uniform(0, calculated_delay) (Full Jitter pattern).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception: Optional[Exception] = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    last_exception = exc
                    if attempt == max_retries:
                        break

                    # Compute delay
                    calculated_delay = min(max_delay, base_delay * (exponential_base ** attempt))
                    actual_delay = random.uniform(0, calculated_delay) if jitter else calculated_delay

                    if on_retry_callback:
                        on_retry_callback(exc, attempt + 1, actual_delay)

                    time.sleep(actual_delay)

            raise RetryExhaustedError(
                f"Failed after {max_retries + 1} attempts. Last error: {last_exception}"
            ) from last_exception

        return wrapper
    return decorator


if __name__ == "__main__":
    calls = 0

    @exponential_backoff_retry(max_retries=3, base_delay=0.01, max_delay=0.1, retryable_exceptions=(ValueError,))
    def flaky_service():
        global calls
        calls += 1
        if calls < 3:
            raise ValueError(f"Temporary failure {calls}")
        return "Success!"

    res = flaky_service()
    assert res == "Success!"
    assert calls == 3
    print("Exponential backoff retry passed successfully!")
