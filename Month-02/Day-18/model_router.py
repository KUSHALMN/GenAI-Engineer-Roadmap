"""
Rule-Based Model Router (Small vs Large Model Routing).
Routes incoming user queries to either a low-cost high-speed small model
or an advanced high-intelligence frontier model based on complexity heuristics.
"""

from typing import Any, Dict, List
from provider_interface import LLMProvider, MockLargeModelProvider, MockSmallModelProvider


class ModelRouter:
    """Intelligently routes requests between Small and Large model tiers."""

    COMPLEX_REASONING_INDICATORS = [
        "derive",
        "proof",
        "refactor",
        "debug",
        "architecture",
        "write code",
        "step-by-step",
        "calculate trajectory",
        "system design",
    ]

    SIMPLE_INDICATORS = [
        "translate",
        "sentiment",
        "format as json",
        "extract keywords",
        "summarize briefly",
        "classify",
    ]

    def __init__(self, small_model: LLMProvider, large_model: LLMProvider):
        self.small_model = small_model
        self.large_model = large_model
        self.routing_stats = {"small_model_routes": 0, "large_model_routes": 0}

    def assess_complexity(self, query: str) -> str:
        """
        Heuristic classification:
        - Returns 'large' if query contains reasoning indicators or length > 500 chars
        - Returns 'small' if matching simple indicators
        - Defaults to 'small' for short queries (< 100 chars)
        """
        q_lower = query.lower()

        # Check reasoning triggers
        if any(ind in q_lower for ind in self.COMPLEX_REASONING_INDICATORS):
            return "large"

        # Check length
        if len(query) > 500:
            return "large"

        # Check simple triggers
        if any(ind in q_lower for ind in self.SIMPLE_INDICATORS):
            return "small"

        return "small"

    def route_and_generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Routes prompt to selected model tier and records routing telemetry."""
        decision = self.assess_complexity(prompt)

        if decision == "large":
            self.routing_stats["large_model_routes"] += 1
            result = self.large_model.generate(prompt, **kwargs)
        else:
            self.routing_stats["small_model_routes"] += 1
            result = self.small_model.generate(prompt, **kwargs)

        result["_routing_decision"] = decision
        return result

    def get_stats(self) -> Dict[str, Any]:
        total = sum(self.routing_stats.values())
        return {
            "total_queries": total,
            "small_model_percentage": round((self.routing_stats["small_model_routes"] / max(total, 1)) * 100, 2),
            "large_model_percentage": round((self.routing_stats["large_model_routes"] / max(total, 1)) * 100, 2),
        }


if __name__ == "__main__":
    router = ModelRouter(MockSmallModelProvider(), MockLargeModelProvider())

    # Simple task -> small
    r1 = router.route_and_generate("Classify the sentiment of this review: 'Great app!'")
    assert r1["_routing_decision"] == "small"
    assert "SmallModel" in r1["text"]

    # Complex task -> large
    r2 = router.route_and_generate("Write code to refactor our microservice architecture")
    assert r2["_routing_decision"] == "large"
    assert "LargeModel" in r2["text"]

    print("ModelRouter Stats:", router.get_stats())
    print("ModelRouter tests passed successfully!")
