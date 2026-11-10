"""
CD & Release Strategy: Progressive Delivery, Canary Traffic Splitting,
Automated Metric Guardrails, and Instant Rollback Triggers.
"""

from dataclasses import dataclass


@dataclass
class DeploymentTarget:
    version: str
    weight_percentage: int # e.g. 10 for 10%
    error_count: int = 0
    total_requests: int = 0

    def error_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.error_count / self.total_requests


class CanaryDeploymentRouter:
    def __init__(self, stable_version: str, canary_version: str, canary_weight: int = 10, error_threshold: float = 0.05):
        self.stable = DeploymentTarget(stable_version, 100 - canary_weight)
        self.canary = DeploymentTarget(canary_version, canary_weight)
        self.error_threshold = error_threshold
        self.rolled_back = False

    def route_request(self, request_index: int) -> str:
        if self.rolled_back:
            return self.stable.version
        # Modulo traffic split
        if (request_index % 100) < self.canary.weight_percentage:
            return self.canary.version
        return self.stable.version

    def record_outcome(self, version: str, is_error: bool):
        target = self.canary if version == self.canary.version else self.stable
        target.total_requests += 1
        if is_error:
            target.error_count += 1

        # Check guardrails
        if version == self.canary.version and target.total_requests >= 20:
            if target.error_rate() > self.error_threshold:
                self.rolled_back = True


if __name__ == "__main__":
    router = CanaryDeploymentRouter(stable_version="v1.0.0", canary_version="v1.1.0", canary_weight=20)
    # Simulate canary failure spike
    for i in range(25):
        v = router.route_request(i)
        is_err = (v == "v1.1.0") # Simulate 100% error on canary
        router.record_outcome(v, is_err)

    assert router.rolled_back is True
    assert router.route_request(10) == "v1.0.0" # Traffic forced to stable
    print("=== Day 14: Progressive Canary Release Router ===")
    print("Automated canary rollback guardrail verified.")
