"""Timeout handling decorators for synchronous and asynchronous tasks."""
import asyncio
import functools
import concurrent.futures
from typing import Callable, Any


class TimeoutException(Exception):
    """Raised when an operation exceeds its configured deadline."""
    pass


def with_timeout(seconds: float):
    """Decorator applying a timeout to async or sync functions."""
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
                except asyncio.TimeoutError:
                    raise TimeoutException(f"Operation '{func.__name__}' timed out after {seconds}s")
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(func, *args, **kwargs)
                    try:
                        return future.result(timeout=seconds)
                    except concurrent.futures.TimeoutError:
                        raise TimeoutException(f"Operation '{func.__name__}' timed out after {seconds}s")
            return sync_wrapper
    return decorator
