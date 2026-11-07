"""
Day 25: Model Routing Evaluation
Routes requests across model tiers (Small 3B vs Medium 8B vs Large 70B)
based on task complexity, measuring routing cost savings vs accuracy retention.
"""

from typing import Dict, Any, List

class ModelTierRouter:
    @staticmethod
    def route_request(prompt: str) -> Dict[str, Any]:
        p_lower = prompt.lower()
        # Complex multi-step reasoning / math -> Tier 1 (70B)
        if any(w in p_lower for w in ["prove", "theorem", "quantum", "architect"]):
            return {"tier": "LARGE_70B", "cost_per_1k": 0.015, "model": "Llama-3-70B"}
        # Extraction / formatting / simple QA -> Tier 3 (3B)
        elif any(w in p_lower for w in ["json", "format", "extract", "capitalize", "translate"]):
            return {"tier": "SMALL_3B", "cost_per_1k": 0.0005, "model": "Llama-3.2-3B"}
        # General conversational -> Tier 2 (8B)
        return {"tier": "MEDIUM_8B", "cost_per_1k": 0.002, "model": "Llama-3-8B"}

if __name__ == "__main__":
    router = ModelTierRouter()
    r1 = router.route_request("Extract email and phone number as JSON")
    assert r1["tier"] == "SMALL_3B"

    r2 = router.route_request("Prove the Riemann Hypothesis theorem")
    assert r2["tier"] == "LARGE_70B"

    print("Model Router Decisions:")
    print(f"Extraction task -> {r1['model']} (Cost: ${r1['cost_per_1k']}/1k)")
    print(f"Reasoning task  -> {r2['model']} (Cost: ${r2['cost_per_1k']}/1k)")
    print("Day 25 AI Model Router Evaluation passed all tests.")
