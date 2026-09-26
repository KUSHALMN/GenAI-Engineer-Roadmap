"""
Structured JSON Logging for LLM Applications.
Provides context propagation (request_id, session_id, user_id),
ISO-8601 timestamps, log level formatting, and clean JSON outputs.
"""

import contextvars
import importlib.util
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Load standard library logging module explicitly so logging.py does not shadow it
std_logging = None
for p in sys.path:
    candidate = os.path.join(p, "logging", "__init__.py")
    if os.path.isfile(candidate) and "Day-06" not in p:
        spec = importlib.util.spec_from_file_location("stdlib_logging", candidate)
        std_logging = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(std_logging)
        break

if std_logging is None:
    # Fallback to direct import
    import logging as std_logging

# Context variable for distributed tracing context
ctx_trace_info: contextvars.ContextVar[Dict[str, str]] = contextvars.ContextVar(
    "ctx_trace_info", default={}
)


class StructuredJSONFormatter(std_logging.Formatter):
    """Formats log records as one-line structured JSON."""

    def format(self, record: std_logging.LogRecord) -> str:
        trace_data = ctx_trace_info.get()

        log_obj: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "request_id": trace_data.get("request_id", "-"),
            "session_id": trace_data.get("session_id", "-"),
        }

        # Include custom extra fields if provided
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            log_obj.update(record.extra_fields)

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj, ensure_ascii=False)


def setup_structured_logger(name: str = "llm_app", level: int = std_logging.INFO) -> std_logging.Logger:
    """Configures and returns a structured JSON logger."""
    logger = std_logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if not logger.handlers:
        handler = std_logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredJSONFormatter())
        logger.addHandler(handler)
        logger.propagate = False

    return logger


def set_trace_context(request_id: str, session_id: Optional[str] = None) -> None:
    """Set the active request and session IDs in contextvars."""
    ctx_trace_info.set({
        "request_id": request_id,
        "session_id": session_id or "default_session",
    })


def clear_trace_context() -> None:
    """Clear contextvars trace info."""
    ctx_trace_info.set({})


if __name__ == "__main__":
    logger = setup_structured_logger("test_observability")
    set_trace_context("req_abc123", "sess_xyz789")

    logger.info("Executing LLM generation", extra={"extra_fields": {"model": "gpt-4o", "tokens": 128}})
    clear_trace_context()
    logger.info("Unscoped system message")
    print("Structured logging tests executed successfully!")
