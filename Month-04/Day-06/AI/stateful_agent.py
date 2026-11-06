"""
Day 06: Stateful Agent Design
Implements typed, immutable state transitions for agent execution,
including messages, execution memory, tool cache, and state transition validation.
"""

from dataclasses import dataclass, field, replace
from typing import List, Dict, Any, Optional
from enum import Enum
import json

class AgentStatus(str, Enum):
    IDLE = "IDLE"
    THINKING = "THINKING"
    EXECUTING_TOOL = "EXECUTING_TOOL"
    AWAITING_INPUT = "AWAITING_INPUT"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass(frozen=True)
class AgentState:
    session_id: str
    status: AgentStatus = AgentStatus.IDLE
    messages: List[Dict[str, str]] = field(default_factory=list)
    tool_cache: Dict[str, Any] = field(default_factory=dict)
    active_plan: List[str] = field(default_factory=list)
    step_count: int = 0
    max_steps: int = 10

    def add_message(self, role: str, content: str) -> "AgentState":
        new_msgs = list(self.messages) + [{"role": role, "content": content}]
        return replace(self, messages=new_msgs, step_count=self.step_count + 1)

    def transition_to(self, new_status: AgentStatus) -> "AgentState":
        # Validate state machine transitions
        allowed_transitions = {
            AgentStatus.IDLE: [AgentStatus.THINKING, AgentStatus.FAILED],
            AgentStatus.THINKING: [AgentStatus.EXECUTING_TOOL, AgentStatus.COMPLETED, AgentStatus.FAILED, AgentStatus.AWAITING_INPUT],
            AgentStatus.EXECUTING_TOOL: [AgentStatus.THINKING, AgentStatus.FAILED],
            AgentStatus.AWAITING_INPUT: [AgentStatus.THINKING, AgentStatus.FAILED],
            AgentStatus.COMPLETED: [],
            AgentStatus.FAILED: []
        }
        if new_status not in allowed_transitions.get(self.status, []):
            raise ValueError(f"Illegal state transition from {self.status} to {new_status}")
        return replace(self, status=new_status)

    def cache_tool_result(self, tool_call_id: str, result: Any) -> "AgentState":
        new_cache = dict(self.tool_cache)
        new_cache[tool_call_id] = result
        return replace(self, tool_cache=new_cache)

if __name__ == "__main__":
    state = AgentState(session_id="session-001")
    assert state.status == AgentStatus.IDLE

    # Valid transitions
    state = state.transition_to(AgentStatus.THINKING)
    state = state.add_message("user", "Analyze Q4 revenue")
    state = state.transition_to(AgentStatus.EXECUTING_TOOL)
    state = state.cache_tool_result("call_1", {"revenue": 5000000})
    state = state.transition_to(AgentStatus.THINKING)
    state = state.add_message("assistant", "Q4 revenue was $5,000,000.")
    state = state.transition_to(AgentStatus.COMPLETED)

    assert state.status == AgentStatus.COMPLETED
    assert len(state.messages) == 2
    assert state.step_count == 2
    print(f"Final Agent State Status: {state.status}, Steps: {state.step_count}")
    print("Day 06 AI Stateful Agent passed all tests.")
