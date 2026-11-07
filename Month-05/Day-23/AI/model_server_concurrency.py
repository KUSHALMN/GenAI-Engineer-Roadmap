"""
Day 23: Model Server Concurrency
Simulates server queue dynamics, measuring GPU saturation,
queue waiting times, and throughput across increasing concurrency levels.
"""

from typing import Dict, Any, List

class ServerConcurrencySimulator:
    def simulate_concurrency(self, concurrency_levels: List[int]) -> List[Dict[str, Any]]:
        results = []
        gpu_capacity = 32 # Maximum concurrent KV sequences

        for c in concurrency_levels:
            active = min(c, gpu_capacity)
            queued = max(0, c - gpu_capacity)
            saturation_pct = min(100.0, (c / gpu_capacity) * 100)
            latency_multiplier = 1.0 + (queued * 0.1)

            results.append({
                "concurrency": c,
                "active_gpu_requests": active,
                "queued_requests": queued,
                "gpu_saturation_pct": round(saturation_pct, 1),
                "relative_latency": round(latency_multiplier, 2)
            })
        return results

if __name__ == "__main__":
    sim = ServerConcurrencySimulator()
    metrics = sim.simulate_concurrency([8, 16, 32, 64])
    assert metrics[2]["gpu_saturation_pct"] == 100.0
    assert metrics[3]["queued_requests"] == 32
    print("Server Concurrency Profile:")
    for m in metrics:
        print(m)
    print("Day 23 AI Model Server Concurrency passed all tests.")
