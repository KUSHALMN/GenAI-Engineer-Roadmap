"""Agent State schema and immutable transitions."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class AgentStatus(Enum):
    INITIALIZED = "INITIALIZED"
    PLANNING = "PLANNING"
    EXECUTING_TOOL = "EXECUTING_TOOL"
    REFLECTING = "REFLECTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class ToolExecutionStep:
    tool_name: str
    arguments: Dict[str, Any]
    result: Any
    latency_ms: float = 0.0


@dataclass
class AgentState:
    session_id: str
    user_goal: str
    status: AgentStatus = AgentStatus.INITIALIZED
    current_step: int = 0
    max_steps: int = 5
    scratchpad: List[str] = field(default_factory=list)
    tool_history: List[ToolExecutionStep] = field(default_factory=list)
    final_answer: Optional[str] = None
    error_message: Optional[str] = None

    def add_thought(self, thought: str):
        self.scratchpad.append(f"Thought: {thought}")

    def add_tool_step(self, tool_name: str, args: Dict[str, Any], result: Any, latency_ms: float = 0.0):
        step = ToolExecutionStep(tool_name, args, result, latency_ms)
        self.tool_history.append(step)
        self.scratchpad.append(f"Action: {tool_name}({args}) -> Result: {result}")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d
