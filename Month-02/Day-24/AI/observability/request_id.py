"""Request ID Context & Propagation for Observability."""
import contextvars
import uuid
from typing import Optional

# Context variable to hold request_id across async and sync call stacks
_request_id_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("request_id", default=None)


def generate_request_id(prefix: str = "req_") -> str:
    """Generate a unique request identifier."""
    return f"{prefix}{uuid.uuid4().hex[:12]}"


def set_request_id(request_id: Optional[str] = None) -> str:
    """Set the active request ID in the current execution context."""
    req_id = request_id or generate_request_id()
    _request_id_ctx.set(req_id)
    return req_id


def get_request_id() -> str:
    """Retrieve the current request ID or generate a default one."""
    req_id = _request_id_ctx.get()
    if not req_id:
        req_id = set_request_id()
    return req_id


def clear_request_id() -> None:
    """Clear request ID from context."""
    _request_id_ctx.set(None)
