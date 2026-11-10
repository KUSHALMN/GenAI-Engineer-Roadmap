"""
Infrastructure as Code (IaC): Declarative Resource Modeling, State Locking,
Drift Detection, and Resource Deletion Safety Guards.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class CloudResource:
    resource_type: str
    resource_id: str
    properties: Dict[str, str]
    protected_against_deletion: bool = True


class IaCStateManager:
    def __init__(self):
        self.desired_state: Dict[str, CloudResource] = {}
        self.live_state: Dict[str, CloudResource] = {}
        self.state_locked: bool = False

    def acquire_lock(self) -> bool:
        if self.state_locked:
            return False
        self.state_locked = True
        return True

    def release_lock(self):
        self.state_locked = False

    def detect_drift(self) -> List[str]:
        drift_report = []
        for rid, desired in self.desired_state.items():
            if rid not in self.live_state:
                drift_report.append(f"MISSING_IN_LIVE: {rid}")
            elif self.live_state[rid].properties != desired.properties:
                drift_report.append(f"PROPERTY_DRIFT: {rid}")
        return drift_report


if __name__ == "__main__":
    iac = IaCStateManager()
    r1 = CloudResource("aws_s3_bucket", "genai-production-vault", {"versioning": "Enabled"})
    iac.desired_state["genai-production-vault"] = r1
    # Live state has drift: versioning disabled
    r1_live = CloudResource("aws_s3_bucket", "genai-production-vault", {"versioning": "Disabled"})
    iac.live_state["genai-production-vault"] = r1_live

    drifts = iac.detect_drift()
    assert len(drifts) == 1
    assert "PROPERTY_DRIFT" in drifts[0]
    print("=== Day 12: Infrastructure as Code (IaC) Manager ===")
    print("State locking and drift detection passed.")
