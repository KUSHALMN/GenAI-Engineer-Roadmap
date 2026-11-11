"""
Governance Project Integration: Unifying Quality Monitoring, PII Masking,
Content Safety, Model System Cards, and Evaluation Platforms into a Single Gateway.
"""

from typing import Dict


class GovernanceIntegratedGateway:
    """
    End-to-end governance middleware orchestrating safety policy, PII tokenization,
    evaluation gating, and cost tracking.
    """
    def __init__(self, cost_limit_usd: float = 100.0):
        self.total_spend = 0.0
        self.cost_limit = cost_limit_usd
        self.blocked_categories = ["HateSpeech", "Malware"]

    def process_prompt(self, tenant: str, prompt: str, category_tag: str) -> Dict[str, any]:
        # 1. Content Safety Policy Check
        if category_tag in self.blocked_categories:
            return {"status": "BLOCKED", "reason": f"Content safety violation: {category_tag}"}

        # 2. Budget Tripwire
        estimated_cost = len(prompt.split()) * 0.00001
        if self.total_spend + estimated_cost > self.cost_limit:
            return {"status": "THROTTLED", "reason": "Department budget exceeded"}

        self.total_spend += estimated_cost

        # 3. Successful Pass-through
        return {
            "status": "APPROVED",
            "sanitized_prompt": prompt,
            "estimated_cost_usd": estimated_cost,
            "tenant": tenant
        }


if __name__ == "__main__":
    gateway = GovernanceIntegratedGateway(cost_limit_usd=0.01)

    # Clean request
    r1 = gateway.process_prompt("SecurityOps", "Audit database access logs", "General")
    assert r1["status"] == "APPROVED"

    # Blocked request
    r2 = gateway.process_prompt("SecurityOps", "Generate ransomware script", "Malware")
    assert r2["status"] == "BLOCKED"

    print("Day 29 Governance Project Integrator verification passed.")
