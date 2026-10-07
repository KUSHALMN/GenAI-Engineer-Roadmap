"""Structured JSON Logger for GenAI Production Systems."""
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from .request_id import get_request_id


class JSONFormatter(logging.Formatter):
    """Formats log records into single-line JSON with context propagation."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", get_request_id()),
        }

        # Include extra metadata fields passed in extra={}
        if hasattr(record, "metadata") and isinstance(record.metadata, dict):
            log_entry["metadata"] = record.metadata

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def get_logger(name: str = "genai.observability") -> logging.Logger:
    """Creates or gets configured structured JSON logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


def log_event(logger: logging.Logger, level: str, message: str, **metadata):
    """Helper to log structured payload with context."""
    req_id = get_request_id()
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message, extra={"request_id": req_id, "metadata": metadata})
