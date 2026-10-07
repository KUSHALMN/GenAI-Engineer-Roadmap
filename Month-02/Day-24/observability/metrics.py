"""Metrics aggregator for LLM observability (latency percentiles, error rates, throughput)."""
import math
from typing import List, Dict, Any


class MetricsAggregator:
    """Collects system latencies, status codes, and computes p50, p95, p99 percentiles."""

    def __init__(self):
        self.latencies: List[float] = []
        self.success_count = 0
        self.failure_count = 0
        self.retrieval_scores: List[float] = []

    def record_call(self, latency_ms: float, success: bool = True):
        self.latencies.append(latency_ms)
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

    def record_retrieval(self, score: float):
        self.retrieval_scores.append(score)

    def _percentile(self, values: List[float], p: float) -> float:
        if not values:
            return 0.0
        sorted_vals = sorted(values)
        k = (len(sorted_vals) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return round(sorted_vals[int(k)], 2)
        d0 = sorted_vals[int(f)] * (c - k)
        d1 = sorted_vals[int(c)] * (k - f)
        return round(d0 + d1, 2)

    def compute_summary(self) -> Dict[str, Any]:
        total_calls = self.success_count + self.failure_count
        error_rate = (self.failure_count / total_calls * 100) if total_calls > 0 else 0.0

        return {
            "total_requests": total_calls,
            "success_rate_pct": round(100.0 - error_rate, 2),
            "error_rate_pct": round(error_rate, 2),
            "latency": {
                "min_ms": round(min(self.latencies), 2) if self.latencies else 0.0,
                "max_ms": round(max(self.latencies), 2) if self.latencies else 0.0,
                "avg_ms": round(sum(self.latencies) / len(self.latencies), 2) if self.latencies else 0.0,
                "p50_ms": self._percentile(self.latencies, 50),
                "p95_ms": self._percentile(self.latencies, 95),
                "p99_ms": self._percentile(self.latencies, 99),
            },
            "avg_retrieval_score": round(
                sum(self.retrieval_scores) / len(self.retrieval_scores), 4
            ) if self.retrieval_scores else 0.0,
        }
