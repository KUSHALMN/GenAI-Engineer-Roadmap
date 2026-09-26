"""
Observability Metrics Summary Generator.
Aggregates trace logs and request records to produce operational reports
covering throughput, error rates, token economics, and latency SLA distributions.
"""

from typing import Any, Dict, List
from latency_tracker import LatencyTracker


class MetricsReportGenerator:

    # Standard per-1K token pricing for reporting
    PRICING_TABLE = {
        "gpt-4o": {"input": 0.0025, "output": 0.010},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "llama-3-8b": {"input": 0.00008, "output": 0.00008},
        "default": {"input": 0.001, "output": 0.002},
    }

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def record_request(
        self,
        request_id: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_latency_ms: float,
        ttft_ms: float = 0.0,
        status: str = "success",
    ) -> None:
        """Add completed request telemetry entry."""
        self.records.append({
            "request_id": request_id,
            "model": model.lower(),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "total_latency_ms": total_latency_ms,
            "ttft_ms": ttft_ms,
            "status": status,
        })

    def generate_summary(self) -> Dict[str, Any]:
        """Aggregate all metrics into an executive telemetry report."""
        if not self.records:
            return {"total_requests": 0, "status": "no data"}

        total_reqs = len(self.records)
        successful_reqs = sum(1 for r in self.records if r["status"] == "success")
        error_rate = (total_reqs - successful_reqs) / total_reqs

        total_prompt_tok = sum(r["prompt_tokens"] for r in self.records)
        total_comp_tok = sum(r["completion_tokens"] for r in self.records)
        total_tokens = total_prompt_tok + total_comp_tok

        latencies = [r["total_latency_ms"] for r in self.records]
        ttfts = [r["ttft_ms"] for r in self.records if r["ttft_ms"] > 0]

        latency_percentiles = LatencyTracker.calculate_percentiles(latencies)
        ttft_percentiles = LatencyTracker.calculate_percentiles(ttfts) if ttfts else {}

        # Compute cost
        total_cost = 0.0
        for r in self.records:
            pricing = self.PRICING_TABLE.get(r["model"], self.PRICING_TABLE["default"])
            total_cost += (r["prompt_tokens"] / 1000.0) * pricing["input"]
            total_cost += (r["completion_tokens"] / 1000.0) * pricing["output"]

        return {
            "traffic": {
                "total_requests": total_reqs,
                "successful_requests": successful_reqs,
                "error_rate_pct": round(error_rate * 100, 2),
            },
            "token_usage": {
                "prompt_tokens": total_prompt_tok,
                "completion_tokens": total_comp_tok,
                "total_tokens": total_tokens,
                "avg_tokens_per_request": round(total_tokens / total_reqs, 1),
            },
            "cost_estimate_usd": round(total_cost, 5),
            "latency_sla_ms": {
                "e2e": latency_percentiles,
                "ttft": ttft_percentiles,
            },
        }


if __name__ == "__main__":
    rep = MetricsReportGenerator()
    rep.record_request("req_1", "gpt-4o-mini", 120, 45, 340.0, 110.0, "success")
    rep.record_request("req_2", "gpt-4o-mini", 200, 80, 410.0, 130.0, "success")
    rep.record_request("req_3", "gpt-4o", 500, 150, 850.0, 220.0, "success")
    rep.record_request("req_4", "gpt-4o-mini", 80, 0, 50.0, 0.0, "error")

    summary = rep.generate_summary()
    print("Report Summary:", summary)
    assert summary["traffic"]["total_requests"] == 4
    assert summary["traffic"]["error_rate_pct"] == 25.0
    print("MetricsReportGenerator tests passed successfully!")
