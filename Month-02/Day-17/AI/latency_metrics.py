"""
Inference Latency & Throughput Metrics Calculator.
Measures TTFT (Time To First Token), ITL (Inter-Token Latency),
Tokens Per Second (TPS), and P50/P90/P95/P99 distributions.
"""

from typing import Dict, List, Optional


class InferenceMetrics:

    @staticmethod
    def calculate_throughput(total_tokens: int, duration_seconds: float) -> float:
        """Calculates generation throughput in tokens per second."""
        if duration_seconds <= 0:
            return 0.0
        return round(total_tokens / duration_seconds, 2)

    @staticmethod
    def calculate_itl(token_timestamps: List[float]) -> Dict[str, float]:
        """Calculates inter-token latency statistics (ms) from sequential arrival timestamps."""
        if len(token_timestamps) < 2:
            return {"mean_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0}

        intervals_ms = [
            (token_timestamps[i] - token_timestamps[i - 1]) * 1000.0
            for i in range(1, len(token_timestamps))
        ]
        sorted_intervals = sorted(intervals_ms)
        n = len(sorted_intervals)

        mean_val = sum(sorted_intervals) / n
        p50 = sorted_intervals[int(round(0.50 * (n - 1)))]
        p95 = sorted_intervals[int(round(0.95 * (n - 1)))]

        return {
            "mean_ms": round(mean_val, 2),
            "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2),
        }

    @staticmethod
    def summarize_request(
        ttft_ms: float,
        total_latency_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> Dict[str, any]:
        """Summarizes a single generation request."""
        generation_duration_sec = max(0.001, (total_latency_ms - ttft_ms) / 1000.0)
        tps = completion_tokens / generation_duration_sec

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "ttft_ms": round(ttft_ms, 2),
            "total_latency_ms": round(total_latency_ms, 2),
            "generation_tps": round(tps, 2),
        }


if __name__ == "__main__":
    summary = InferenceMetrics.summarize_request(
        ttft_ms=120.0,
        total_latency_ms=620.0,
        prompt_tokens=256,
        completion_tokens=50,
    )
    print("Inference Metric Summary:", summary)
    assert summary["ttft_ms"] == 120.0
    assert summary["generation_tps"] == 100.0
    print("Inference metrics tests passed successfully!")
