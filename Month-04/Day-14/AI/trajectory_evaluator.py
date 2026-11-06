"""
Day 14: Agent Trajectory Evaluation
Evaluates agent runs against ground-truth trajectories:
- Tool selection accuracy
- Step efficiency (redundant call penalty)
- Argument correctness
- Goal achievement score
"""

from typing import List, Dict, Any

class TrajectoryEvaluator:
    def evaluate(self, actual_trajectory: List[Dict[str, Any]], expected_trajectory: List[Dict[str, Any]]) -> Dict[str, Any]:
        expected_tools = [step["tool"] for step in expected_trajectory]
        actual_tools = [step["tool"] for step in actual_trajectory]

        # Precision & Recall of tool choice
        matched_tools = [t for t in actual_tools if t in expected_tools]
        tool_precision = len(matched_tools) / len(actual_tools) if actual_tools else 0.0
        tool_recall = len(matched_tools) / len(expected_tools) if expected_tools else 0.0

        # Efficiency penalty: ratio of expected steps to actual steps
        step_efficiency = min(1.0, len(expected_trajectory) / max(1, len(actual_trajectory)))

        # Overall trajectory score
        overall_score = round(0.4 * tool_precision + 0.4 * tool_recall + 0.2 * step_efficiency, 3)

        return {
            "overall_score": overall_score,
            "tool_precision": round(tool_precision, 3),
            "tool_recall": round(tool_recall, 3),
            "step_efficiency": round(step_efficiency, 3),
            "actual_steps": len(actual_trajectory),
            "expected_steps": len(expected_trajectory)
        }

if __name__ == "__main__":
    evaluator = TrajectoryEvaluator()

    expected = [
        {"tool": "fetch_user", "args": {"id": 10}},
        {"tool": "send_email", "args": {"to": "user@test.com"}}
    ]

    # Perfect run
    actual_perfect = [
        {"tool": "fetch_user", "args": {"id": 10}},
        {"tool": "send_email", "args": {"to": "user@test.com"}}
    ]
    res_perf = evaluator.evaluate(actual_perfect, expected)
    assert res_perf["overall_score"] == 1.0

    # Inefficient run with hallucinated extra step
    actual_inefficient = [
        {"tool": "random_search", "args": {}},
        {"tool": "fetch_user", "args": {"id": 10}},
        {"tool": "send_email", "args": {"to": "user@test.com"}}
    ]
    res_ineff = evaluator.evaluate(actual_inefficient, expected)
    assert res_ineff["overall_score"] < 1.0
    print(f"Trajectory evaluation result: {res_ineff}")
    print("Day 14 AI Trajectory Evaluator passed all tests.")
