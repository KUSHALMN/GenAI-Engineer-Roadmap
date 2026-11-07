"""
Day 17: Inference vs Training Deep Dive
Models the two distinct phases of LLM generation:
1. Prefill Phase (Compute-bound: parallel matrix multiplication over prompt tokens)
2. Decode Phase (Memory bandwidth-bound: sequential auto-regressive next-token generation)
Calculates Time-To-First-Token (TTFT) and Time-Per-Output-Token (TPOT).
"""

from typing import Dict, Any

class InferencePhaseSimulator:
    @staticmethod
    def simulate_latency(prompt_tokens: int,
                          gen_tokens: int,
                          flops_tflops: float = 300.0,
                          memory_bandwidth_gbs: float = 800.0,
                          model_params_billions: float = 7.0) -> Dict[str, float]:
        # Prefill: Compute-bound ~ 2 * params * prompt_tokens FLOPS
        prefill_flops = 2.0 * (model_params_billions * 1e9) * prompt_tokens
        ttft_sec = prefill_flops / (flops_tflops * 1e12)

        # Decode: Memory bandwidth-bound ~ reading weights per token
        # Bytes per token = model_params * 2 bytes (FP16)
        decode_bytes_per_token = model_params_billions * 2.0 * 1e9
        tpot_sec = decode_bytes_per_token / (memory_bandwidth_gbs * 1e9)

        total_latency_sec = ttft_sec + (tpot_sec * gen_tokens)

        return {
            "ttft_ms": round(ttft_sec * 1000, 2),
            "tpot_ms": round(tpot_sec * 1000, 2),
            "total_latency_sec": round(total_latency_sec, 3),
            "throughput_tokens_per_sec": round(gen_tokens / total_latency_sec, 1)
        }

if __name__ == "__main__":
    sim = InferencePhaseSimulator()
    metrics = sim.simulate_latency(prompt_tokens=512, gen_tokens=128)
    print("Inference Phase Latency Analysis (7B Model):")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    assert metrics["ttft_ms"] > 0
    assert metrics["tpot_ms"] > 0
    print("Day 17 AI Prefill vs Decode Benchmark passed all tests.")
