"""
Quality-Latency-Cost (QLC) Pareto Optimization: Finding the Non-dominated Frontier
Across Model Families, Quantization Levels, Prompt Compressions, and Routing Policies.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ServingCandidate:
    name: str
    quality_score: float # 0.0 to 1.0 (Higher is better)
    latency_p95_ms: float # Lower is better
    cost_per_k_requests_usd: float # Lower is better


class ParetoOptimizationEngine:
    """
    Computes the Pareto Optimal frontier across multi-objective trade-offs.
    """
    def find_pareto_frontier(self, candidates: List[ServingCandidate]) -> List[ServingCandidate]:
        frontier = []
        for i, c1 in enumerate(candidates):
            dominated = False
            for j, c2 in enumerate(candidates):
                if i == j:
                    continue
                # c2 dominates c1 if c2 is >= in quality AND <= in latency & cost, and strictly better in at least one
                if (c2.quality_score >= c1.quality_score and
                    c2.latency_p95_ms <= c1.latency_p95_ms and
                    c2.cost_per_k_requests_usd <= c1.cost_per_k_requests_usd):
                    if (c2.quality_score > c1.quality_score or
                        c2.latency_p95_ms < c1.latency_p95_ms or
                        c2.cost_per_k_requests_usd < c1.cost_per_k_requests_usd):
                        dominated = True
                        break
            if not dominated:
                frontier.append(c1)
        return frontier


if __name__ == "__main__":
    engine = ParetoOptimizationEngine()
    models = [
        ServingCandidate("Llama-3-70B-FP16", 0.92, 1200.0, 15.0),
        ServingCandidate("Llama-3-70B-INT4", 0.90, 450.0, 4.5), # Fast & cheap, slight quality drop
        ServingCandidate("Llama-3-8B-FP16", 0.81, 300.0, 1.5),
        ServingCandidate("Inefficient-Legacy-Model", 0.75, 1400.0, 20.0), # Strictly dominated
        ServingCandidate("Gemini-Flash-Optimized", 0.89, 180.0, 0.8) # Frontier champion
    ]

    frontier = engine.find_pareto_frontier(models)
    print("Pareto Optimal Configurations:")
    for f in frontier:
        print(f" -> {f.name}: Quality={f.quality_score}, P95={f.latency_p95_ms}ms, Cost=${f.cost_per_k_requests_usd}")
    
    names = [f.name for f in frontier]
    assert "Inefficient-Legacy-Model" not in names
    assert "Gemini-Flash-Optimized" in names
    print("Day 22 Pareto Optimization Engine verification passed.")
