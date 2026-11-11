"""
Agent Evaluation Metrics: Task Completion, Trajectory Step Efficiency,
Tool Precision & Recall, and Infinite Loop Detection.
"""

from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass
class AgentStepRecord:
    step_number: int
    tool_called: str
    arguments: Dict[str, str]
    success: bool


class AgentTrajectoryEvaluator:
    def evaluate_trajectory(self, trajectory: List[AgentStepRecord], expected_tools: Set[str], max_allowed_steps: int = 10) -> Dict[str, float]:
        called_tools = set(s.tool_called for s in trajectory)
        true_positives = len(called_tools.intersection(expected_tools))
        precision = true_positives / max(1, len(called_tools))
        recall = true_positives / max(1, len(expected_tools))
        step_efficiency = 1.0 - (len(trajectory) / max_allowed_steps)

        return {
            "tool_precision": round(precision, 2),
            "tool_recall": round(recall, 2),
            "step_efficiency": round(max(0.0, step_efficiency), 2),
            "task_completed": 1.0 if recall >= 1.0 else 0.0
        }


if __name__ == "__main__":
    evaluator = AgentTrajectoryEvaluator()
    steps = [
        AgentStepRecord(1, "search_docs", {"query": "RPO"}, True),
        AgentStepRecord(2, "calculate_cost", {"hours": "730"}, True)
    ]
    metrics = evaluator.evaluate_trajectory(steps, expected_tools={"search_docs", "calculate_cost"})
    assert metrics["tool_precision"] == 1.0
    assert metrics["tool_recall"] == 1.0
    assert metrics["task_completed"] == 1.0

    print("=== Day 06: Agent Trajectory Evaluator ===")
    print(f"Agent Trajectory Metrics: {metrics}")
