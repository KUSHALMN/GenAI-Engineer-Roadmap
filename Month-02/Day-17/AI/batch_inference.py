"""
Continuous Dynamic Batching vs Sequential Inference Simulator.
Demonstrates GPU throughput multipliers, KV Cache memory overhead,
and latency tradeoff curves under batched concurrency.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class InferenceJob:
    job_id: str
    prompt_tokens: int
    max_new_tokens: int
    generated_tokens: int = 0
    finished: bool = False


class BatchInferenceSimulator:

    @staticmethod
    def calculate_kv_cache_bytes(
        batch_size: int,
        seq_length: int,
        num_layers: int = 32,
        num_kv_heads: int = 8,
        head_dim: int = 128,
        bytes_per_elem: int = 2,  # FP16
    ) -> int:
        """
        Calculates KV Cache memory in bytes:
        KV Memory = 2 (keys+values) * num_layers * num_kv_heads * head_dim * seq_length * batch_size * bytes_per_element
        """
        return 2 * num_layers * num_kv_heads * head_dim * seq_length * batch_size * bytes_per_elem

    @classmethod
    def compare_sequential_vs_batched(cls, num_requests: int = 16, avg_tokens: int = 60) -> Dict[str, Any]:
        """
        Simulates execution time and throughput for:
        1. Sequential processing (batch_size = 1)
        2. Continuous dynamic batching (batch_size = 8)
        """
        # Time per token generation step in milliseconds
        step_latency_seq_ms = 12.0  # single stream step
        step_latency_batched_ms = 16.0  # slight GPU compute overhead for batch=8

        total_tokens = num_requests * avg_tokens

        # 1. Sequential: processes 1 request at a time
        total_time_seq_ms = num_requests * (avg_tokens * step_latency_seq_ms)
        tps_seq = total_tokens / (total_time_seq_ms / 1000.0)

        # 2. Batched (batch_size = 8): 2 batches of 8 requests
        batch_size = 8
        num_batches = (num_requests + batch_size - 1) // batch_size
        total_time_batched_ms = num_batches * (avg_tokens * step_latency_batched_ms)
        tps_batched = total_tokens / (total_time_batched_ms / 1000.0)

        # KV Cache memory at max sequence length (e.g. 512 tokens)
        kv_cache_mb = cls.calculate_kv_cache_bytes(batch_size=batch_size, seq_length=512) / (1024 * 1024)

        return {
            "num_requests": num_requests,
            "total_tokens_generated": total_tokens,
            "sequential": {
                "total_time_sec": round(total_time_seq_ms / 1000.0, 2),
                "throughput_tps": round(tps_seq, 1),
            },
            "dynamic_batched": {
                "batch_size": batch_size,
                "total_time_sec": round(total_time_batched_ms / 1000.0, 2),
                "throughput_tps": round(tps_batched, 1),
                "kv_cache_usage_mb": round(kv_cache_mb, 2),
            },
            "throughput_gain_factor": round(tps_batched / max(tps_seq, 0.001), 2),
        }


if __name__ == "__main__":
    sim = BatchInferenceSimulator()
    comparison = sim.compare_sequential_vs_batched(num_requests=16, avg_tokens=50)
    print("Batching Comparison Result:", comparison)
    assert comparison["throughput_gain_factor"] > 4.0
    print("BatchInferenceSimulator tests passed successfully!")
