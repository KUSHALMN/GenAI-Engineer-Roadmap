"""
AI Governance, Model System Cards & Auditability: Automated Generation of Model Cards,
Dataset Lineage Tracking, Intended Use, Risk Mitigations, and Compliance Artifacts.
"""

from dataclasses import asdict, dataclass, field
import json
from typing import Dict, List


@dataclass
class IntendedUsePolicy:
    primary_intended_uses: List[str]
    out_of_scope_use_cases: List[str]
    target_users: List[str]


@dataclass
class RiskMitigationStrategy:
    risk_category: str
    severity: str
    mitigation_mechanism: str
    residual_risk_level: str


@dataclass
class ModelSystemCard:
    model_name: str
    model_version: str
    release_date: str
    intended_use: IntendedUsePolicy
    training_data_summary: Dict[str, str]
    evaluation_benchmarks: Dict[str, float]
    risk_mitigations: List[RiskMitigationStrategy] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


class GovernanceAuditManager:
    """
    Validates model system card completeness and compliance readiness against EU AI Act
    and internal risk frameworks.
    """
    def __init__(self):
        self.registry: Dict[str, ModelSystemCard] = {}

    def register_card(self, card: ModelSystemCard) -> bool:
        # Mandatory fields validation
        if not card.intended_use.primary_intended_uses:
            raise ValueError("Intended uses must not be empty.")
        if not card.intended_use.out_of_scope_use_cases:
            raise ValueError("Out of scope use cases must be declared.")
        if not card.risk_mitigations:
            raise ValueError("At least one risk mitigation must be documented.")
        
        self.registry[f"{card.model_name}:{card.model_version}"] = card
        return True

    def audit_readiness_score(self, model_key: str) -> float:
        card = self.registry.get(model_key)
        if not card:
            return 0.0
        score = 0.0
        if len(card.intended_use.out_of_scope_use_cases) >= 2: score += 25.0
        if len(card.evaluation_benchmarks) >= 3: score += 25.0
        if len(card.risk_mitigations) >= 2: score += 25.0
        if "data_provenance" in card.training_data_summary: score += 25.0
        return score


if __name__ == "__main__":
    manager = GovernanceAuditManager()
    card = ModelSystemCard(
        model_name="EnterpriseAgenticRAG",
        model_version="v2.4.0",
        release_date="2026-11-15",
        intended_use=IntendedUsePolicy(
            primary_intended_uses=["Internal enterprise knowledge search", "Automated ticket triage"],
            out_of_scope_use_cases=["Direct medical diagnosis", "Automated legal advice without review"],
            target_users=["Support Engineers", "DevOps Specialists"]
        ),
        training_data_summary={
            "data_provenance": "Curated internal confluence docs and git repos",
            "license_filtered": "True",
            "pii_scrubbed": "True"
        },
        evaluation_benchmarks={
            "ragas_faithfulness": 0.94,
            "ragas_answer_relevance": 0.91,
            "safety_refusal_rate": 0.99
        },
        risk_mitigations=[
            RiskMitigationStrategy("Prompt Injection", "High", "Dual Guardrail Token Classifier", "Low"),
            RiskMitigationStrategy("PII Leakage", "Critical", "Surrogate Tokenization Vault", "Negligible")
        ]
    )

    manager.register_card(card)
    score = manager.audit_readiness_score("EnterpriseAgenticRAG:v2.4.0")
    print("System Card JSON:")
    print(card.to_json())
    print("Audit Readiness Score:", score)
    assert score == 100.0
    print("AI Governance System Card verification passed.")
