"""
Observability Middleware & Pipeline Instrumentation for LLM APIs.
Wraps LLM and tool calls with automated span tracking, token accounting,
and contextual structured logging.
"""

import functools
import time
import uuid
from typing import Any, Callable, Dict, List, Optional
from latency_tracker import LatencyTracker
from logging import clear_trace_context, set_trace_context, setup_structured_logger


logger = setup_structured_logger("observability_middleware")


class LLMTracer:
    """
    Manages end-to-end tracing across an LLM request lifecycle.
    """

    def __init__(self, request_id: Optional[str] = None, session_id: Optional[str] = None):
        self.request_id = request_id or f"req_{uuid.uuid4().hex[:10]}"
        self.session_id = session_id or f"sess_{uuid.uuid4().hex[:8]}"
        self.tracker = LatencyTracker()
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.events: List[Dict[str, Any]] = []

    def __enter__(self):
        set_trace_context(self.request_id, self.session_id)
        logger.info("Starting request execution", extra={"extra_fields": {"stage": "init"}})
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        status = "failed" if exc_type else "completed"
        extra = {
            "status": status,
            "total_tokens": self.total_tokens,
            "latency_summary": self.tracker.get_summary(),
        }
        if exc_val:
            extra["error"] = str(exc_val)
            logger.error("Request execution failed", extra={"extra_fields": extra})
        else:
            logger.info("Request execution finished", extra={"extra_fields": extra})
        clear_trace_context()

    @property
    def total_tokens(self) -> int:
        return self.total_prompt_tokens + self.total_completion_tokens

    def trace_span(self, span_name: str, metadata: Optional[Dict[str, Any]] = None):
        """Context manager for tracing a custom sub-span (retrieval, tool, etc.)."""
        class SpanContext:
            def __init__(self, outer, name, meta):
                self.outer = outer
                self.name = name
                self.meta = meta or {}

            def __enter__(self):
                self.outer.tracker.start_span(self.name, self.meta)
                logger.info(f"Span '{self.name}' started", extra={"extra_fields": {"span": self.name, **self.meta}})
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                status = "error" if exc_type else "ok"
                span = self.outer.tracker.end_span(self.name, {"status": status})
                logger.info(
                    f"Span '{self.name}' ended",
                    extra={"extra_fields": {"span": self.name, "duration_ms": span.duration_ms if span else 0, "status": status}}
                )

        return SpanContext(self, span_name, metadata)

    def record_llm_tokens(self, prompt_tokens: int, completion_tokens: int) -> None:
        """Accumulate token usage."""
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens


def observe_llm_call(model_name: str = "gpt-4o-mini"):
    """Decorator to automatically instrument an LLM inference function."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, tracer: Optional[LLMTracer] = None, **kwargs):
            if tracer is None:
                tracer = LLMTracer()

            with tracer:
                with tracer.trace_span("llm_inference", {"model": model_name}):
                    result = func(*args, **kwargs)
                    usage = result.get("usage", {})
                    tracer.record_llm_tokens(
                        prompt_tokens=usage.get("prompt_tokens", 0),
                        completion_tokens=usage.get("completion_tokens", 0),
                    )
                    return result
        return wrapper
    return decorator


if __name__ == "__main__":
    tracer = LLMTracer()

    with tracer:
        with tracer.trace_span("vector_retrieval", {"top_k": 3}):
            time.sleep(0.02)

        with tracer.trace_span("tool_execution", {"tool": "calculator"}):
            time.sleep(0.01)

        tracer.record_llm_tokens(prompt_tokens=150, completion_tokens=45)

    assert tracer.total_tokens == 195
    print("Observability middleware passed successfully!")
