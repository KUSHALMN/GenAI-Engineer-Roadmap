"""
Policy Enforcement & Content Safety: Multi-category Safety Taxonomy, Rule-based &
Heuristic Policy Gates, Violations Scorer, and Action Enforcement (Pass, Flag, Block, Escalate).
"""

from dataclasses import dataclass
from enum import Enum
import re
from typing import List, Set


class PolicyAction(Enum):
    ALLOW = "ALLOW"
    FLAG = "FLAG"
    BLOCK = "BLOCK"
    ESCALATE = "ESCALATE"


@dataclass
class PolicyRule:
    category: str
    patterns: List[str]
    severity: int # 1 to 5
    default_action: PolicyAction


@dataclass
class PolicyEvaluationResult:
    action: PolicyAction
    triggered_categories: Set[str]
    max_severity: int
    rationale: str


class ContentSafetyPolicyEngine:
    """
    Evaluates inbound requests and model outputs against enterprise acceptable use policies (AUP).
    """
    def __init__(self):
        self.rules: List[PolicyRule] = []
        self._compiled_patterns: List[Tuple[PolicyRule, List[re.Pattern]]] = []

    def add_rule(self, rule: PolicyRule):
        compiled = [re.compile(p, re.IGNORECASE) for p in rule.patterns]
        self._compiled_patterns.append((rule, compiled))

    def evaluate(self, content: str) -> PolicyEvaluationResult:
        triggered: Set[str] = set()
        max_severity = 0
        final_action = PolicyAction.ALLOW

        for rule, patterns in self._compiled_patterns:
            for pattern in patterns:
                if pattern.search(content):
                    triggered.add(rule.category)
                    if rule.severity > max_severity:
                        max_severity = rule.severity
                    if rule.default_action.value > final_action.value: # BLOCK > FLAG > ALLOW
                        final_action = rule.default_action
                    break

        # Action escalation logic based on severity
        if max_severity >= 5:
            final_action = PolicyAction.BLOCK
        elif max_severity >= 3 and final_action == PolicyAction.ALLOW:
            final_action = PolicyAction.FLAG

        rationale = f"Policy decision: {final_action.value}. Triggered: {list(triggered) if triggered else 'None'}"
        return PolicyEvaluationResult(
            action=final_action,
            triggered_categories=triggered,
            max_severity=max_severity,
            rationale=rationale
        )


if __name__ == "__main__":
    engine = ContentSafetyPolicyEngine()
    engine.add_rule(PolicyRule(
        category="HateSpeech",
        patterns=[r"\bhate\s+all\s+\w+\b", r"\bexterminate\s+\w+\b"],
        severity=5,
        default_action=PolicyAction.BLOCK
    ))
    engine.add_rule(PolicyRule(
        category="CompetitorMention",
        patterns=[r"\bcompetitorX\b", r"\brivalcorp\b"],
        severity=2,
        default_action=PolicyAction.FLAG
    ))

    # Test 1: Clean
    res1 = engine.evaluate("Can you summarize our Q3 earnings release?")
    assert res1.action == PolicyAction.ALLOW

    # Test 2: Flag
    res2 = engine.evaluate("How does our product compare to RivalCorp?")
    assert res2.action == PolicyAction.FLAG
    assert "CompetitorMention" in res2.triggered_categories

    # Test 3: Block
    res3 = engine.evaluate("We should hate all rivals and destroy them.")
    assert res3.action == PolicyAction.BLOCK
    assert "HateSpeech" in res3.triggered_categories

    print("Day 18 Content Safety Policy Engine verification passed.")
