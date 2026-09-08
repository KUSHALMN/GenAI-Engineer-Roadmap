import time
import uuid
import math
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from pydantic import BaseModel, Field

class LLMSpan(BaseModel):
    span_id: str
    trace_id: str
    name: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    duration_ms: float = 0.0
    status: str = "ok"
    error_message: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)

class ObservabilityTracer:
    PRICING = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "claude-3-5-sonnet": {"input": 0.003, "output": 0.015}
    }

    def __init__(self):
        self.spans: List[LLMSpan] = []

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        rates = self.PRICING.get(model, self.PRICING["gpt-4o-mini"])
        cost = (prompt_tokens / 1000.0 * rates["input"]) + (completion_tokens / 1000.0 * rates["output"])
        return round(cost, 6)

    @contextmanager
    def start_span(self, name: str, model: str, trace_id: Optional[str] = None):
        tid = trace_id or str(uuid.uuid4())[:8]
        sid = str(uuid.uuid4())[:8]
        span = LLMSpan(span_id=sid, trace_id=tid, name=name, model=model)
        start_t = time.perf_counter()
        try:
            yield span
        except Exception as e:
            span.status = "error"
            span.error_message = str(e)
            raise
        finally:
            span.duration_ms = round((time.perf_counter() - start_t) * 1000.0, 2)
            span.total_tokens = span.prompt_tokens + span.completion_tokens
            span.estimated_cost_usd = self.calculate_cost(
                model, span.prompt_tokens, span.completion_tokens
            )
            self.spans.append(span)

    def get_latency_percentiles(self) -> Dict[str, float]:
        if not self.spans:
            return {"p50": 0.0, "p95": 0.0, "p99": 0.0, "mean": 0.0}

        durations = sorted([s.duration_ms for s in self.spans])
        n = len(durations)

        def percentile(p: float) -> float:
            k = (n - 1) * p
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return durations[int(k)]
            d0 = durations[int(f)] * (c - k)
            d1 = durations[int(c)] * (k - f)
            return round(d0 + d1, 2)

        return {
            "p50": percentile(0.50),
            "p95": percentile(0.95),
            "p99": percentile(0.99),
            "mean": round(sum(durations) / n, 2)
        }

    def get_summary_metrics(self) -> Dict[str, Any]:
        total_prompts = sum(s.prompt_tokens for s in self.spans)
        total_completions = sum(s.completion_tokens for s in self.spans)
        total_cost = sum(s.estimated_cost_usd for s in self.spans)
        total_errors = sum(1 for s in self.spans if s.status == "error")

        return {
            "total_calls": len(self.spans),
            "total_tokens": total_prompts + total_completions,
            "prompt_tokens": total_prompts,
            "completion_tokens": total_completions,
            "total_cost_usd": round(total_cost, 6),
            "error_rate": round(total_errors / max(1, len(self.spans)), 4),
            "latency_percentiles_ms": self.get_latency_percentiles()
        }
