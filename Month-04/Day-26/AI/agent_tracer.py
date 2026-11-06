"""
Day 26: Agent Observability
Implements OpenTelemetry-compatible tracing for AI agents:
Spans for thoughts, tool calls, token usage, latency, and status codes.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import time
import uuid

@dataclass
class Span:
    span_id: str
    trace_id: str
    name: str
    parent_id: Optional[str]
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    status: str = "UNSET"

class AgentTracer:
    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id = trace_id or uuid.uuid4().hex
        self.spans: List[Span] = []

    def start_span(self, name: str, parent_id: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> Span:
        span = Span(
            span_id=uuid.uuid4().hex[:8],
            trace_id=self.trace_id,
            name=name,
            parent_id=parent_id,
            start_time=time.time(),
            attributes=attributes or {}
        )
        self.spans.append(span)
        return span

    def end_span(self, span: Span, status: str = "OK", extra_attributes: Optional[Dict[str, Any]] = None):
        span.end_time = time.time()
        span.status = status
        if extra_attributes:
            span.attributes.update(extra_attributes)

    def get_summary(self) -> Dict[str, Any]:
        total_duration = sum((s.end_time - s.start_time) for s in self.spans if s.end_time)
        total_tokens = sum(s.attributes.get("tokens", 0) for s in self.spans)
        return {
            "trace_id": self.trace_id,
            "total_spans": len(self.spans),
            "total_duration_sec": round(total_duration, 4),
            "total_tokens": total_tokens
        }

if __name__ == "__main__":
    tracer = AgentTracer()

    # Agent root span
    root = tracer.start_span("agent_run", attributes={"goal": "Retrieve stock data"})

    # Thought span
    thought_span = tracer.start_span("think", parent_id=root.span_id, attributes={"tokens": 120})
    time.sleep(0.01)
    tracer.end_span(thought_span, "OK")

    # Tool span
    tool_span = tracer.start_span("tool:get_stock", parent_id=root.span_id, attributes={"ticker": "MSFT"})
    time.sleep(0.02)
    tracer.end_span(tool_span, "OK", {"result_bytes": 1024})

    tracer.end_span(root, "OK")

    summary = tracer.get_summary()
    assert summary["total_spans"] == 3
    assert summary["total_tokens"] == 120
    print(f"Tracer Summary: {summary}")
    print("Day 26 AI Agent Tracer passed all tests.")
