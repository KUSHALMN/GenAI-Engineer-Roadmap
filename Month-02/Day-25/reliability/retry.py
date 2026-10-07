"""Retry mechanisms with backoff integration for transient LLM API errors."""
import time
import functools
from typing import Callable, Tuple, Type
from .backoff import ExponentialBackoff

RETRYABLE_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    ConnectionError,
    TimeoutError,
    RuntimeError,
)


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 0.2,
    max_delay: float = 2.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = RETRYABLE_EXCEPTIONS
):
    """Decorator to retry failing operations with exponential jitter backoff."""
    backoff = ExponentialBackoff(base_delay=base_delay, max_delay=max_delay)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    last_err = exc
                    if attempt == max_retries:
                        break
                    delay = backoff.compute_delay(attempt)
                    time.sleep(delay)
            raise last_err
        return wrapper
    return decorator
