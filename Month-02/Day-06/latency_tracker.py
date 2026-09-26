"""
Fine-Grained Latency & Span Tracker for LLM Applications.
Tracks TTFT (Time To First Token), Inter-token latency, Tool execution, and Vector retrieval spans.
Calculates statistical percentiles (p50, p90, p95, p99).
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Span:
    name: str
    start_time: float
    end_time: Optional[float] = None
    metadata: Dict[str, any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000.0


class LatencyTracker:
    """Tracks latency metrics across execution spans."""

    def __init__(self):
        self.spans: List[Span] = []
        self._active_spans: Dict[str, Span] = {}
        self.ttft_ms: Optional[float] = None

    def start_span(self, name: str, metadata: Optional[Dict[str, any]] = None) -> Span:
        """Begin a named timing span."""
        span = Span(name=name, start_time=time.perf_counter(), metadata=metadata or {})
        self._active_spans[name] = span
        return span

    def end_span(self, name: str, additional_metadata: Optional[Dict[str, any]] = None) -> Optional[Span]:
        """Complete a named timing span."""
        span = self._active_spans.pop(name, None)
        if span:
            span.end_time = time.perf_counter()
            if additional_metadata:
                span.metadata.update(additional_metadata)
            self.spans.append(span)
        return span

    def record_first_token(self, start_time: float) -> float:
        """Record TTFT (Time to first token) in ms."""
        self.ttft_ms = (time.perf_counter() - start_time) * 1000.0
        return self.ttft_ms

    def get_summary(self) -> Dict[str, any]:
        """Produce breakdown of all recorded spans."""
        breakdown = {s.name: round(s.duration_ms, 2) for s in self.spans}
        total_time = sum(s.duration_ms for s in self.spans)
        return {
            "spans_ms": breakdown,
            "total_measured_latency_ms": round(total_time, 2),
            "ttft_ms": round(self.ttft_ms, 2) if self.ttft_ms is not None else None,
        }

    @staticmethod
    def calculate_percentiles(durations_ms: List[float]) -> Dict[str, float]:
        """Calculates p50, p90, p95, p99 for a list of latency values."""
        if not durations_ms:
            return {"p50": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0}

        sorted_vals = sorted(durations_ms)
        n = len(sorted_vals)

        def get_p(p: float) -> float:
            idx = int(round(p * (n - 1)))
            return round(sorted_vals[idx], 2)

        return {
            "p50": get_p(0.50),
            "p90": get_p(0.90),
            "p95": get_p(0.95),
            "p99": get_p(0.99),
        }


if __name__ == "__main__":
    tracker = LatencyTracker()
    tracker.start_span("retrieval", {"chunks": 3})
    time.sleep(0.05)
    tracker.end_span("retrieval")

    tracker.start_span("llm_generation", {"model": "llama-3-8b"})
    time.sleep(0.1)
    tracker.end_span("llm_generation")

    summary = tracker.get_summary()
    print("Latency Summary:", summary)
    assert "retrieval" in summary["spans_ms"]
    assert "llm_generation" in summary["spans_ms"]

    sample_durations = [25.0, 30.0, 35.0, 40.0, 50.0, 80.0, 120.0, 200.0, 350.0, 600.0]
    percentiles = LatencyTracker.calculate_percentiles(sample_durations)
    print("Percentiles:", percentiles)
    assert percentiles["p50"] > 0
    print("LatencyTracker tests passed successfully!")
