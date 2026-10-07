"""Sequential and Conditional Workflow DAG Executor."""
from typing import Callable, Dict, Any, List


class WorkflowStep:
    def __init__(self, name: str, action: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.name = name
        self.action = action


class WorkflowPipeline:
    """Deterministic Multi-Step Pipeline with shared context dictionary."""

    def __init__(self, name: str):
        self.name = name
        self.steps: List[WorkflowStep] = []

    def add_step(self, name: str, action: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.steps.append(WorkflowStep(name, action))
        return self

    def execute(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        state = dict(initial_state)
        history = []
        for step in self.steps:
            output = step.action(state)
            state.update(output)
            history.append(step.name)
        state["_pipeline_history"] = history
        return state
