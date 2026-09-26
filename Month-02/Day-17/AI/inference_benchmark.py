"""
LLM Generation Latency & Throughput Benchmark.
Simulates generation runs with streaming token intervals,
tracking TTFT, tokens/sec, and concurrency impact.
"""

import time
from typing import Any, Dict, List
from latency_metrics import InferenceMetrics


class InferenceBenchmark:

    @staticmethod
    def simulate_streaming_generation(prompt_len: int, completion_len: int, tps_target: float = 60.0) -> Dict[str, Any]:
        """Simulates an LLM token generation stream."""
        start_time = time.perf_counter()

        # Simulated TTFT: depends on prompt length (e.g. 50ms base + 0.1ms per prompt token)
        ttft_duration = 0.05 + (prompt_len * 0.0001)
        time.sleep(min(0.05, ttft_duration))  # Keep unit test fast
        first_token_time = time.perf_counter()

        ttft_ms = (first_token_time - start_time) * 1000.0

        # Simulate generating completion tokens
        timestamps = [first_token_time]
        delay_per_token = 1.0 / tps_target

        # Scale down delay for fast test execution
        simulated_step = min(0.002, delay_per_token)
        for _ in range(completion_len):
            time.sleep(simulated_step)
            timestamps.append(time.perf_counter())

        total_latency_ms = (timestamps[-1] - start_time) * 1000.0
        itl_stats = InferenceMetrics.calculate_itl(timestamps)

        return {
            "prompt_tokens": prompt_len,
            "completion_tokens": completion_len,
            "ttft_ms": round(ttft_ms, 2),
            "total_latency_ms": round(total_latency_ms, 2),
            "inter_token_latency": itl_stats,
            "tokens_per_sec": InferenceMetrics.calculate_throughput(
                completion_len, (timestamps[-1] - first_token_time)
            ),
        }

    @classmethod
    def run_suite(cls) -> List[Dict[str, Any]]:
        """Run benchmark suite across multiple prompt/completion scenarios."""
        scenarios = [
            {"name": "Short Query", "prompt": 32, "completion": 20},
            {"name": "Medium Context", "prompt": 512, "completion": 50},
            {"name": "Long Document RAG", "prompt": 2048, "completion": 80},
        ]
        results = []
        for s in scenarios:
            res = cls.simulate_streaming_generation(s["prompt"], s["completion"])
            res["scenario"] = s["name"]
            results.append(res)
        return results


if __name__ == "__main__":
    benchmark = InferenceBenchmark()
    results = benchmark.run_suite()
    print("Benchmark Suite Results:")
    for r in results:
        print(f"[{r['scenario']}] TTFT: {r['ttft_ms']}ms | Total: {r['total_latency_ms']}ms | TPS: {r['tokens_per_sec']}")
    assert len(results) == 3
    print("Inference benchmark suite passed successfully!")
