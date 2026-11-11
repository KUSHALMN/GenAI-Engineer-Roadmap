"""
Online Quality Monitoring: Production Output Sampling, User Feedback Logging
(Thumbs Up/Down), Latency Tracking, and Automated Quality Drift Alarms.
"""

from dataclasses import dataclass, field
import time
from typing import List, Optional


@dataclass
class ProductionInteractionRecord:
    session_id: str
    prompt: str
    response: str
    user_feedback: Optional[int] # 1 for thumbs-up, -1 for thumbs-down, None for unrated
    latency_ms: float
    timestamp: float = field(default_factory=time.time)


class OnlineQualityMonitor:
    def __init__(self, satisfaction_alarm_threshold: float = 0.85):
        self.interactions: List[ProductionInteractionRecord] = []
        self.satisfaction_threshold = satisfaction_alarm_threshold

    def record_interaction(self, record: ProductionInteractionRecord):
        self.interactions.append(record)

    def calculate_satisfaction_rate(self) -> float:
        rated = [r for r in self.interactions if r.user_feedback is not None]
        if not rated:
            return 1.0
        positive = sum(1 for r in rated if r.user_feedback == 1)
        return round(positive / len(rated), 2)

    def is_alarm_triggered(self) -> bool:
        return self.calculate_satisfaction_rate() < self.satisfaction_threshold


if __name__ == "__main__":
    monitor = OnlineQualityMonitor(satisfaction_alarm_threshold=0.80)
    monitor.record_interaction(ProductionInteractionRecord("s_1", "What is RPO?", "Max data loss", 1, 45.0))
    monitor.record_interaction(ProductionInteractionRecord("s_2", "Explain DR", "Disaster recovery", 1, 50.0))
    monitor.record_interaction(ProductionInteractionRecord("s_3", "Explain RTO?", "Wrong response", -1, 55.0))

    sat_rate = monitor.calculate_satisfaction_rate()
    assert sat_rate == 0.67
    assert monitor.is_alarm_triggered() is True

    print("=== Day 11: Online Quality Monitor ===")
    print(f"Satisfaction Rate: {sat_rate*100:.1f}% | Alarm Triggered: {monitor.is_alarm_triggered()}")
