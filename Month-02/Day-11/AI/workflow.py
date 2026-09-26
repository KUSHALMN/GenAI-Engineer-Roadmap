"""
Deterministic Sequential Workflow Engine.
Executes a strictly ordered pipeline of transforms and validation steps without LLM agent loops.
Ideal for high-reliability, low-latency, and predictable business processes.
"""

import time
from typing import Any, Callable, Dict, List, Optional


class WorkflowStep:
    def __init__(self, name: str, action: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.name = name
        self.action = action


class SequentialWorkflow:
    """Deterministic step-by-step pipeline."""

    def __init__(self, name: str = "LinearPipeline"):
        self.name = name
        self.steps: List[WorkflowStep] = []

    def add_step(self, name: str, action: Callable[[Dict[str, Any]], Dict[str, Any]]) -> "SequentialWorkflow":
        """Add step to the execution pipeline."""
        self.steps.append(WorkflowStep(name, action))
        return self

    def execute(self, initial_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Runs each step in sequence, passing state forward."""
        state = dict(initial_payload)
        execution_trace = []

        start_total = time.perf_counter()

        for step in self.steps:
            t0 = time.perf_counter()
            try:
                state = step.action(state)
                duration_ms = (time.perf_counter() - t0) * 1000
                execution_trace.append({"step": step.name, "status": "success", "duration_ms": round(duration_ms, 2)})
            except Exception as e:
                duration_ms = (time.perf_counter() - t0) * 1000
                execution_trace.append({"step": step.name, "status": "error", "error": str(e), "duration_ms": round(duration_ms, 2)})
                state["_workflow_status"] = "failed"
                state["_failed_step"] = step.name
                state["_error"] = str(e)
                state["_trace"] = execution_trace
                return state

        state["_workflow_status"] = "completed"
        state["_trace"] = execution_trace
        state["_total_duration_ms"] = round((time.perf_counter() - start_total) * 1000, 2)
        return state


# Example standard document processing workflow
def step_clean_text(data: Dict[str, Any]) -> Dict[str, Any]:
    text = data.get("raw_text", "").strip()
    data["cleaned_text"] = " ".join(text.split())
    return data

def step_extract_entities(data: Dict[str, Any]) -> Dict[str, Any]:
    text = data["cleaned_text"]
    words = text.split()
    data["word_count"] = len(words)
    data["is_long"] = len(words) > 10
    return data

def step_format_response(data: Dict[str, Any]) -> Dict[str, Any]:
    data["result"] = f"Processed {data['word_count']} words. Category: {'Long' if data['is_long'] else 'Short'}"
    return data


if __name__ == "__main__":
    pipeline = SequentialWorkflow("DocProcessor")
    pipeline.add_step("clean", step_clean_text)
    pipeline.add_step("extract", step_extract_entities)
    pipeline.add_step("format", step_format_response)

    res = pipeline.execute({"raw_text": "  Hello world from    Antigravity  workflow engine!  "})
    print("Workflow Result:", res)
    assert res["_workflow_status"] == "completed"
    assert res["word_count"] == 6
    assert "Processed 6 words" in res["result"]
    print("Sequential workflow tests passed successfully!")
