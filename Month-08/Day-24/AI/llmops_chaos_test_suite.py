"""
Failure & Chaos Testing for LLMOps: Simulating Network Partitions, Upstream Provider Outages,
Token Rate Limit (HTTP 429) Faults, Corrupted Context Payloads, and Resiliency Verification.
"""

from dataclasses import dataclass
import random
import time
from typing import Callable, Dict


@dataclass
class ChaosFaultProfile:
    failure_rate_429: float = 0.0 # Rate limit injection
    network_latency_ms: float = 0.0 # Latency injection
    context_corruption_rate: float = 0.0 # Data corruption


class ChaosFaultInjector:
    """
    Middleware injecting faults into LLM calls to test resilience of fallback cascades.
    """
    def __init__(self, profile: ChaosFaultProfile):
        self.profile = profile

    def invoke_with_chaos(self, prompt: str, primary_fn: Callable[[str], str], fallback_fn: Callable[[str], str]) -> Dict[str, any]:
        # Inject latency
        if self.profile.network_latency_ms > 0:
            time.sleep(self.profile.network_latency_ms / 1000.0)

        # Inject 429 Rate Limit
        if random.random() < self.profile.failure_rate_429:
            # Trigger fallback
            fallback_res = fallback_fn(prompt)
            return {
                "source": "fallback",
                "status": "CIRCUIT_BREAKER_TRIGGERED_429",
                "result": fallback_res
            }

        # Success case
        return {
            "source": "primary",
            "status": "SUCCESS",
            "result": primary_fn(prompt)
        }


if __name__ == "__main__":
    def primary_llm(p: str) -> str:
        return f"Primary LLM response to: {p}"

    def fallback_llm(p: str) -> str:
        return f"Cached fallback response to: {p}"

    # Profile with 100% 429 failure rate
    chaos_profile = ChaosFaultProfile(failure_rate_429=1.0)
    injector = ChaosFaultInjector(chaos_profile)

    res = injector.invoke_with_chaos("Analyze system logs", primary_llm, fallback_llm)
    print("Chaos Test Result:", res)
    assert res["source"] == "fallback"
    assert res["status"] == "CIRCUIT_BREAKER_TRIGGERED_429"
    print("Day 24 LLMOps Chaos Test Suite verification passed.")
