"""
Evaluation Strategy and Quality Dimensions: Multi-Dimensional Metrics Mapping,
Correctness, Groundedness, Completeness, Safety, Helpfulness, Latency, and Cost.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class QualityMetricScore:
    dimension: str
    target_threshold: float
    actual_score: float
    passed: bool


class EvaluationStrategyPlanner:
    def __init__(self, thresholds: Dict[str, float]):
        self.thresholds = thresholds

    def evaluate_dimension(self, dimension: str, measured_score: float) -> QualityMetricScore:
        target = self.thresholds.get(dimension, 0.8)
        passed = measured_score >= target
        return QualityMetricScore(dimension, target, measured_score, passed)

    def evaluate_system(self, measurements: Dict[str, float]) -> List[QualityMetricScore]:
        return [self.evaluate_dimension(dim, score) for dim, score in measurements.items()]


if __name__ == "__main__":
    thresholds = {
        "correctness": 0.90,
        "groundedness": 0.95,
        "completeness": 0.85,
        "safety": 0.99,
        "helpfulness": 0.88
    }
    planner = EvaluationStrategyPlanner(thresholds)
    system_results = {
        "correctness": 0.92,
        "groundedness": 0.96,
        "completeness": 0.89,
        "safety": 1.00,
        "helpfulness": 0.91
    }
    scores = planner.evaluate_system(system_results)
    assert all(s.passed for s in scores)

    print("=== Day 01: Evaluation Strategy Planner ===")
    print(f"Evaluated {len(scores)} Quality Dimensions. All Passed: True")
