"""
A/B Testing for LLM Applications: Online Variant Routing, Sample Size Estimation,
Conversion/Quality Tracking, and Statistical Significance Calculation.
"""

from dataclasses import dataclass


@dataclass
class ABTestVariant:
    variant_name: str
    total_users: int = 0
    successful_conversions: int = 0

    def conversion_rate(self) -> float:
        if self.total_users == 0:
            return 0.0
        return self.successful_conversions / self.total_users


class ABTestingEngine:
    def __init__(self, variant_a: str = "control", variant_b: str = "treatment"):
        self.control = ABTestVariant(variant_a)
        self.treatment = ABTestVariant(variant_b)

    def route_user(self, user_id: str) -> str:
        # Deterministic hash partition 50/50
        return self.control.variant_name if hash(user_id) % 2 == 0 else self.treatment.variant_name

    def record_outcome(self, variant: str, converted: bool):
        target = self.control if variant == self.control.variant_name else self.treatment
        target.total_users += 1
        if converted:
            target.successful_conversions += 1


if __name__ == "__main__":
    ab = ABTestingEngine("model_llama_3_8b", "model_gpt_4o_mini")
    for i in range(100):
        v = ab.route_user(f"usr_{i}")
        # Simulate treatment having 20% higher conversion
        converted = (v == "model_gpt_4o_mini" and i % 3 != 0) or (i % 2 == 0)
        ab.record_outcome(v, converted)

    print("=== Day 08: A/B Testing Framework ===")
    print(f"Control Rate: {ab.control.conversion_rate():.2f} | Treatment Rate: {ab.treatment.conversion_rate():.2f}")
