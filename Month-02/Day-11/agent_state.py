"""
Agent State Management.
Maintains state, scratchpad, step history, and execution context across iterations.
"""

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentStep:
    iteration: int
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class AgentState:
    query: str
    session_id: str
    current_iteration: int = 0
    status: str = "initialized"  # "running", "completed", "failed", "max_iterations"
    steps: List[AgentStep] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    final_answer: Optional[str] = None
    error: Optional[str] = None

    def add_step(
        self,
        thought: str,
        action: Optional[str] = None,
        action_input: Optional[Dict[str, Any]] = None,
        observation: Optional[str] = None,
    ) -> None:
        """Record step taken by the agent."""
        self.current_iteration += 1
        step = AgentStep(
            iteration=self.current_iteration,
            thought=thought,
            action=action,
            action_input=action_input,
            observation=observation,
        )
        self.steps.append(step)

    def get_scratchpad(self) -> str:
        """Format history of thought/action/observation for prompt inclusion."""
        lines = []
        for s in self.steps:
            lines.append(f"Thought: {s.thought}")
            if s.action:
                lines.append(f"Action: {s.action}({json.dumps(s.action_input or {})})")
            if s.observation:
                lines.append(f"Observation: {s.observation}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state for persistence/checkpoints."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentState":
        """Deserialize state from checkpoint."""
        steps_data = data.pop("steps", [])
        state = cls(**data)
        state.steps = [AgentStep(**s) for s in steps_data]
        return state


if __name__ == "__main__":
    state = AgentState(query="What is 15 * 4?", session_id="sess_01")
    state.add_step(thought="I need to multiply 15 by 4", action="calculator", action_input={"a": 15, "b": 4}, observation="60")
    assert state.current_iteration == 1
    assert "calculator" in state.get_scratchpad()
    serialized = state.to_dict()
    restored = AgentState.from_dict(serialized)
    assert restored.session_id == "sess_01"
    assert len(restored.steps) == 1
    print("AgentState tests passed successfully!")
