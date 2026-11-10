"""
Observability Platform Integration: Distributed W3C Trace Context,
OpenTelemetry-Compatible Spans, Latency Tracking, and Token Attributes.
"""

from dataclasses import dataclass, field
import time
import uuid
from typing import Any, Dict, List, Optional


@dataclass
class TraceSpan:
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def duration_ms(self) -> float:
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000


class OpenTelemetryTracer:
    def __init__(self):
        self.spans: List[TraceSpan] = []

    def start_span(self, name: str, trace_id: Optional[str] = None, parent_span_id: Optional[str] = None) -> TraceSpan:
        t_id = trace_id or str(uuid.uuid4()).replace("-", "")[:16]
        s_id = str(uuid.uuid4()).replace("-", "")[:8]
        span = TraceSpan(
            trace_id=t_id,
            span_id=s_id,
            parent_span_id=parent_span_id,
            name=name,
            start_time=time.perf_counter()
        )
        self.spans.append(span)
        return span

    def end_span(self, span: TraceSpan, attributes: Optional[Dict[str, Any]] = None):
        span.end_time = time.perf_counter()
        if attributes:
            span.attributes.update(attributes)


if __name__ == "__main__":
    tracer = OpenTelemetryTracer()
    parent = tracer.start_span("api.request")
    child = tracer.start_span("llm.generation", trace_id=parent.trace_id, parent_span_id=parent.span_id)
    time.sleep(0.01) # Emulate model generation
    tracer.end_span(child, {"model": "llama-3-8b", "tokens_generated": 142})
    tracer.end_span(parent, {"http.status": 200})

    assert child.parent_span_id == parent.span_id
    assert child.duration_ms() > 5.0
    print("=== Day 18: OpenTelemetry Tracer ===")
    print(f"Recorded Span '{child.name}' Duration: {child.duration_ms():.2f}ms")
