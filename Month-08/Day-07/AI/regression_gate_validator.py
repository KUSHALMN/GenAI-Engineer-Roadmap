"""
Automated Regression Gates: Quality Gate Evaluation, Baseline vs Candidate Comparison,
and CI Deployment Blocking on Metric Regressions.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RegressionGateResult:
    passed: bool
    regressed_metrics: List[str]
    improvements: List[str]


class RegressionGateValidator:
    def __init__(self, max_allowed_regression: float = 0.02):
        self.max_allowed_regression = max_allowed_regression

    def evaluate_gate(self, baseline: Dict[str, float], candidate: Dict[str, float]) -> RegressionGateResult:
        regressed = []
        improved = []
        for metric, base_val in baseline.items():
            cand_val = candidate.get(metric, 0.0)
            diff = cand_val - base_val
            if diff < -self.max_allowed_regression:
                regressed.append(f"{metric} dropped by {abs(diff):.3f}")
            elif diff > 0.01:
                improved.append(f"{metric} gained by {diff:.3f}")

        return RegressionGateResult(
            passed=len(regressed) == 0,
            regressed_metrics=regressed,
            improvements=improved
        )


if __name__ == "__main__":
    gate = RegressionGateValidator(max_allowed_regression=0.02)
    baseline = {"accuracy": 0.94, "faithfulness": 0.96}
    # Candidate drops faithfulness from 0.96 to 0.91 (> 0.02 regression)
    candidate = {"accuracy": 0.95, "faithfulness": 0.91}
    res = gate.evaluate_gate(baseline, candidate)
    assert res.passed is False
    assert len(res.regressed_metrics) == 1

    print("=== Day 07: Automated Regression Gate ===")
    print(f"Gate Passed: {res.passed} | Regressed: {res.regressed_metrics}")
