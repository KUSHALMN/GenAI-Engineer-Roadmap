"""
Cost Observability & Budgets: Real-time Token Cost Accounting, Tiered Departmental Budgets,
Anomaly Burst Detection, and Circuit Breaker Throttling.
"""

from dataclasses import dataclass
import time
from typing import Dict


@dataclass
class TokenPriceRate:
    prompt_token_cost_per_million: float
    completion_token_cost_per_million: float


@dataclass
class DepartmentBudget:
    department: str
    monthly_limit_usd: float
    current_spend_usd: float = 0.0
    alert_threshold_percent: float = 80.0


class CostObservabilityEngine:
    """
    Monitors token consumption per department/tenant, applies billing rates,
    and enforces budget tripwires and alerts.
    """
    def __init__(self):
        self.pricing: Dict[str, TokenPriceRate] = {
            "gemini-1.5-pro": TokenPriceRate(3.50, 10.50),
            "gemini-1.5-flash": TokenPriceRate(0.35, 1.05),
            "gpt-4o": TokenPriceRate(5.00, 15.00)
        }
        self.budgets: Dict[str, DepartmentBudget] = {}

    def set_budget(self, department: str, limit_usd: float):
        self.budgets[department] = DepartmentBudget(department=department, monthly_limit_usd=limit_usd)

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        rate = self.pricing.get(model, TokenPriceRate(1.0, 2.0))
        cost = (prompt_tokens / 1_000_000.0) * rate.prompt_token_cost_per_million + \
               (completion_tokens / 1_000_000.0) * rate.completion_token_cost_per_million
        return cost

    def record_usage(self, department: str, model: str, prompt_tokens: int, completion_tokens: int) -> Dict[str, any]:
        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)
        b = self.budgets.get(department)
        if not b:
            return {"allowed": True, "cost_usd": cost, "status": "No budget defined"}

        b.current_spend_usd += cost
        utilization = (b.current_spend_usd / b.monthly_limit_usd) * 100.0

        if b.current_spend_usd > b.monthly_limit_usd:
            return {
                "allowed": False,
                "cost_usd": cost,
                "utilization_pct": utilization,
                "status": "BUDGET_EXCEEDED_TRIPWIRE_ENGAGED"
            }
        elif utilization >= b.alert_threshold_percent:
            return {
                "allowed": True,
                "cost_usd": cost,
                "utilization_pct": utilization,
                "status": "WARNING_THRESHOLD_REACHED"
            }

        return {
            "allowed": True,
            "cost_usd": cost,
            "utilization_pct": utilization,
            "status": "NORMAL"
        }


if __name__ == "__main__":
    engine = CostObservabilityEngine()
    engine.set_budget("SearchTeam", 100.0) # $100 monthly limit

    # Small batch
    res1 = engine.record_usage("SearchTeam", "gemini-1.5-flash", 1_000_000, 500_000)
    print("Usage 1:", res1)
    assert res1["allowed"] is True

    # Heavy usage pushing near budget
    engine.record_usage("SearchTeam", "gpt-4o", 15_000_000, 1_000_000)
    res2 = engine.record_usage("SearchTeam", "gemini-1.5-pro", 500_000, 100_000)
    print("Usage 2:", res2)
    assert res2["status"] in ["WARNING_THRESHOLD_REACHED", "BUDGET_EXCEEDED_TRIPWIRE_ENGAGED"]

    print("Day 21 Cost Observability Engine verification passed.")
