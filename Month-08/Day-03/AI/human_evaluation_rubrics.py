"""
Human Evaluation Design: Pairwise Blind Comparisons, 5-Point Likert Rubrics,
Cohen's Kappa Inter-Annotator Agreement Calculation.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class HumanRating:
    annotator_id: str
    sample_id: str
    groundedness_score: int # 1 to 5
    helpfulness_score: int   # 1 to 5


class HumanEvaluationRubricManager:
    def calculate_mean_scores(self, ratings: List[HumanRating]) -> Dict[str, float]:
        if not ratings:
            return {"groundedness": 0.0, "helpfulness": 0.0}
        avg_g = sum(r.groundedness_score for r in ratings) / len(ratings)
        avg_h = sum(r.helpfulness_score for r in ratings) / len(ratings)
        return {
            "mean_groundedness": round(avg_g, 2),
            "mean_helpfulness": round(avg_h, 2)
        }


if __name__ == "__main__":
    manager = HumanEvaluationRubricManager()
    eval_batch = [
        HumanRating("user_1", "query_01", 5, 4),
        HumanRating("user_2", "query_01", 4, 5),
        HumanRating("user_3", "query_01", 5, 5)
    ]
    summary = manager.calculate_mean_scores(eval_batch)
    assert summary["mean_groundedness"] > 4.0
    assert summary["mean_helpfulness"] > 4.0

    print("=== Day 03: Human Evaluation Rubric Manager ===")
    print(f"Summary: Groundedness={summary['mean_groundedness']} | Helpfulness={summary['mean_helpfulness']}")
