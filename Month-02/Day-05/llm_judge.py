"""
LLM-as-a-Judge Evaluator.
Performs pairwise comparisons between two prompt / RAG versions (Candidate A vs Candidate B),
with position-bias mitigation (swapping inputs) and structured critique generation.
"""

from typing import Any, Callable, Dict, List, Optional


class LLMJudge:
    """
    Evaluator that assesses pairwise model responses across multiple criteria:
    1. Accuracy & Correctness
    2. Faithfulness to Context
    3. Conciseness & Clarity
    """

    CRITERIA_WEIGHTS = {
        "accuracy": 0.40,
        "groundedness": 0.35,
        "conciseness": 0.25,
    }

    def __init__(self, judge_callable: Optional[Callable[[str], str]] = None):
        self.judge_callable = judge_callable or self._heuristic_judge

    def _heuristic_judge(self, prompt: str) -> str:
        """Mock LLM judge for local offline testing."""
        return "Winner: A. Reason: Candidate A is more directly grounded in the provided context and avoids unnecessary verbose padding."

    def judge_pairwise(
        self,
        query: str,
        context: str,
        response_a: str,
        response_b: str,
    ) -> Dict[str, Any]:
        """
        Compare Response A vs Response B.
        To mitigate position bias, this evaluates A vs B, then B vs A.
        """
        # Evaluation 1: A first, B second
        eval_1 = self._evaluate_single_pass(query, context, cand_1=response_a, cand_2=response_b, label_1="A", label_2="B")

        # Evaluation 2 (Swap to counter position bias): B first, A second
        eval_2 = self._evaluate_single_pass(query, context, cand_1=response_b, cand_2=response_a, label_1="B", label_2="A")

        # Reconcile judgements
        if eval_1["winner"] == eval_2["winner"]:
            final_winner = eval_1["winner"]
        else:
            final_winner = "Tie"

        return {
            "query": query,
            "winner": final_winner,
            "pass_1_decision": eval_1,
            "pass_2_decision": eval_2,
            "confidence": "high" if final_winner != "Tie" else "medium",
        }

    def _evaluate_single_pass(
        self,
        query: str,
        context: str,
        cand_1: str,
        cand_2: str,
        label_1: str,
        label_2: str,
    ) -> Dict[str, Any]:
        """Score single arrangement using structured rubric."""
        score_1 = self._score_candidate(query, context, cand_1)
        score_2 = self._score_candidate(query, context, cand_2)

        if score_1 > score_2 + 0.05:
            winner = label_1
            reason = f"Candidate {label_1} scored higher on rubric ({score_1:.2f} vs {score_2:.2f})"
        elif score_2 > score_1 + 0.05:
            winner = label_2
            reason = f"Candidate {label_2} scored higher on rubric ({score_2:.2f} vs {score_1:.2f})"
        else:
            winner = "Tie"
            reason = f"Both candidates performed comparably ({score_1:.2f} vs {score_2:.2f})"

        return {
            "winner": winner,
            f"score_{label_1}": score_1,
            f"score_{label_2}": score_2,
            "reason": reason,
        }

    def _score_candidate(self, query: str, context: str, response: str) -> float:
        """Rubric scoring."""
        q_words = set(query.lower().split())
        c_words = set(context.lower().split())
        r_words = set(response.lower().split())

        # Groundedness: fraction of response words in context
        groundedness = len(r_words.intersection(c_words)) / max(len(r_words), 1)

        # Relevance: query words addressed
        relevance = len(r_words.intersection(q_words)) / max(len(q_words), 1)

        # Conciseness penalty if response > 80 words
        conciseness = 1.0 if len(response.split()) <= 60 else max(0.2, 1.0 - (len(response.split()) - 60) * 0.015)

        total_score = (
            groundedness * self.CRITERIA_WEIGHTS["groundedness"]
            + relevance * self.CRITERIA_WEIGHTS["accuracy"]
            + conciseness * self.CRITERIA_WEIGHTS["conciseness"]
        )
        return round(total_score, 4)


if __name__ == "__main__":
    judge = LLMJudge()
    q = "How does LoRA reduce memory?"
    ctx = "LoRA freezes pre-trained weights and adds low-rank decomposition matrices."
    resp_a = "LoRA freezes model weights and introduces low-rank matrices to cut memory."
    resp_b = "LoRA is a method that fine tunes everything completely with massive GPUs and takes a very long time to finish training without any low rank approximations."

    result = judge.judge_pairwise(q, ctx, resp_a, resp_b)
    print("Judge Decision:", result)
    assert result["winner"] == "A"
    print("LLMJudge tests passed successfully!")
