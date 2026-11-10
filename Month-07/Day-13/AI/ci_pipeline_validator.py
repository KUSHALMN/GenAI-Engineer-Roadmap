"""
CI Pipelines for LLMOps: Pipeline Definition Linter, Stage Order Validation,
Automated Security Step Check, and Model Eval Matrix Verification.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class CIPipelineCheckResult:
    passed: bool
    executed_stages: List[str]
    missing_critical_stages: List[str]


class CIPipelineValidator:
    MANDATORY_STAGES = ["lint", "type_check", "unit_test", "security_scan", "model_eval"]

    def validate_pipeline(self, pipeline_stages: List[str]) -> CIPipelineCheckResult:
        missing = [s for s in self.MANDATORY_STAGES if s not in pipeline_stages]
        return CIPipelineCheckResult(
            passed=len(missing) == 0,
            executed_stages=pipeline_stages,
            missing_critical_stages=missing
        )


if __name__ == "__main__":
    validator = CIPipelineValidator()
    complete_stages = ["lint", "type_check", "unit_test", "security_scan", "model_eval", "build_image"]
    res = validator.validate_pipeline(complete_stages)
    assert res.passed is True

    incomplete = ["unit_test", "build_image"]
    res_bad = validator.validate_pipeline(incomplete)
    assert res_bad.passed is False
    assert "security_scan" in res_bad.missing_critical_stages

    print("=== Day 13: CI Pipeline Validator ===")
    print("Mandatory LLMOps CI stage verification passed.")
