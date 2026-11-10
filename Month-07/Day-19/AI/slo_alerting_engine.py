"""
Dashboards and Alerting: Service Level Indicators (SLIs), Service Level Objectives (SLOs),
Error Budget Burn Rate Calculation, and PagerDuty Alert Generation.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AlertNotification:
    severity: str
    metric_name: str
    message: str
    burn_rate: float


class SLOAlertingEngine:
    def __init__(self, target_availability: float = 0.999):
        self.target_availability = target_availability
        self.allowed_error_rate = 1.0 - target_availability

    def calculate_burn_rate(self, total_requests: int, error_requests: int) -> float:
        if total_requests == 0:
            return 0.0
        current_error_rate = error_requests / total_requests
        return current_error_rate / self.allowed_error_rate

    def evaluate_alerts(self, total_requests: int, error_requests: int) -> Optional[AlertNotification]:
        burn_rate = self.calculate_burn_rate(total_requests, error_requests)
        # SRE standard: Burn rate > 14.4x consumes 2% of budget in 1 hour -> Page
        if burn_rate >= 14.4:
            return AlertNotification(
                severity="CRITICAL",
                metric_name="error_budget_burn",
                message=f"Rapid burn rate ({burn_rate:.1f}x) detected on API gateway!",
                burn_rate=burn_rate
            )
        elif burn_rate >= 6.0:
            return AlertNotification(
                severity="WARNING",
                metric_name="error_budget_burn",
                message=f"Elevated error budget burn rate ({burn_rate:.1f}x).",
                burn_rate=burn_rate
            )
        return None


if __name__ == "__main__":
    slo = SLOAlertingEngine(target_availability=0.999) # 99.9% SLO -> allowed error 0.1%
    # 1000 requests with 20 errors -> error rate 2.0% -> burn rate 20x!
    alert = slo.evaluate_alerts(total_requests=1000, error_requests=20)
    assert alert is not None
    assert alert.severity == "CRITICAL"
    print("=== Day 19: SLO Alerting Engine ===")
    print(f"Triggered Alert: [{alert.severity}] {alert.message}")
