"""Latency tracker and timing decorators for LLM/RAG operations."""
import time
import functools
from typing import Callable, Any, Dict, Optional
from .request_id import get_request_id


class LatencyTracker:
    """Records duration and stage checkpoints for execution spans."""

    def __init__(self, operation_name: str, request_id: Optional[str] = None):
        self.operation_name = operation_name
        self.request_id = request_id or get_request_id()
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.duration_ms: float = 0.0
        self.checkpoints: Dict[str, float] = {}

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)

    def mark(self, stage_name: str):
        """Mark an intermediate milestone timestamp."""
        elapsed = round((time.perf_counter() - self.start_time) * 1000, 2)
        self.checkpoints[stage_name] = elapsed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation_name,
            "request_id": self.request_id,
            "duration_ms": self.duration_ms,
            "checkpoints": self.checkpoints,
        }


def timed(operation_name: Optional[str] = None):
    """Decorator to measure and log function duration."""
    def decorator(func: Callable) -> Callable:
        op_name = operation_name or func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
                # Attach latency to result if dict
                if isinstance(locals().get("result"), dict):
                    locals()["result"].setdefault("_meta", {})["latency_ms"] = elapsed_ms
        return wrapper
    return decorator
