"""
LLM-as-a-Judge Calibration: Position Bias Mitigation, Verbosity Bias Detection,
and Judge-Human Agreement Benchmarking.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class JudgeEvaluationPair:
    response_a: str
    response_b: str
    winner_order_1: str # 'A', 'B', 'TIE'
    winner_order_2: str # Evaluated with B first: 'A', 'B', 'TIE'


class LLMJudgeCalibrator:
    def detect_position_bias(self, evals: List[JudgeEvaluationPair]) -> Dict[str, float]:
        consistent = 0
        position_swapped = 0
        for pair in evals:
            if pair.winner_order_1 == pair.winner_order_2:
                consistent += 1
            else:
                position_swapped += 1
        total = max(1, len(evals))
        return {
            "consistency_rate": round(consistent / total, 2),
            "position_bias_rate": round(position_swapped / total, 2)
        }


if __name__ == "__main__":
    calibrator = LLMJudgeCalibrator()
    evals = [
        JudgeEvaluationPair("Short accurate answer", "Long verbose answer", "A", "A"),
        JudgeEvaluationPair("Concise summary", "Detailed explanation", "A", "B") # Swapped when position flipped!
    ]
    bias = calibrator.detect_position_bias(evals)
    assert bias["consistency_rate"] == 0.5
    assert bias["position_bias_rate"] == 0.5

    print("=== Day 04: LLM-as-a-Judge Calibration ===")
    print(f"Calibration Bias Report: {bias}")
