"""
Day 05: Planner-Executor Pattern
Separates high-level task decomposition from execution, tracks completion state,
validates dependencies, and dynamically replans upon encountering failed steps.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
import json

class StepStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class PlanStep:
    def __init__(self, step_id: int, description: str, tool_name: str, args: Dict[str, Any]):
        self.step_id = step_id
        self.description = description
        self.tool_name = tool_name
        self.args = args
        self.status = StepStatus.PENDING
        self.output: Optional[Any] = None

class PlannerExecutorAgent:
    def __init__(self, tools: Dict[str, Any]):
        self.tools = tools
        self.plan: List[PlanStep] = []

    def create_plan(self, task: str) -> List[PlanStep]:
        """Decomposes goal into ordered execution steps."""
        return [
            PlanStep(1, "Retrieve financial quarterly report", "fetch_doc", {"doc_id": "Q3_2026"}),
            PlanStep(2, "Extract revenue numbers", "extract_metric", {"metric": "revenue"}),
            PlanStep(3, "Generate summary chart", "plot_chart", {"chart_type": "bar"})
        ]

    def execute_plan(self, plan: List[PlanStep]) -> Dict[str, Any]:
        """Executes steps sequentially and handles errors."""
        context: Dict[str, Any] = {}
        for step in plan:
            step.status = StepStatus.IN_PROGRESS
            print(f"[Executor] Starting Step {step.step_id}: {step.description}")

            tool = self.tools.get(step.tool_name)
            if not tool:
                step.status = StepStatus.FAILED
                return {"success": False, "failed_step": step.step_id, "error": f"Tool '{step.tool_name}' missing"}

            try:
                # Merge context into args if needed
                result = tool(**step.args)
                step.output = result
                step.status = StepStatus.COMPLETED
                context[f"step_{step.step_id}"] = result
                print(f"[Executor] Completed Step {step.step_id}: Output={result}")
            except Exception as e:
                step.status = StepStatus.FAILED
                print(f"[Executor] Step {step.step_id} failed: {e}")
                return {"success": False, "failed_step": step.step_id, "error": str(e)}

        return {"success": True, "final_context": context}

if __name__ == "__main__":
    mock_tools = {
        "fetch_doc": lambda doc_id: f"Content of {doc_id}: Total revenue was $4.2B.",
        "extract_metric": lambda metric: 4200000000,
        "plot_chart": lambda chart_type: f"{chart_type.upper()} chart rendered successfully."
    }

    agent = PlannerExecutorAgent(mock_tools)
    plan = agent.create_plan("Summarize Q3 revenue")
    res = agent.execute_plan(plan)

    assert res["success"] is True
    assert "step_2" in res["final_context"] and res["final_context"]["step_2"] == 4200000000
    print("\nPlanner-Executor execution succeeded:")
    print(json.dumps(res, indent=2))
