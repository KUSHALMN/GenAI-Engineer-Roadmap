"""
Human-in-the-Loop (HITL) Tool Approval & Agent Max-Iteration Safety Guard.
Enforces human authorization for high-impact actions and bounds agent recursion depth.
"""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    TIMED_OUT = "timed_out"


@dataclass
class ToolExecutionRequest:
    request_id: str
    tool_name: str
    arguments: Dict[str, Any]
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: float = field(default_factory=time.time)
    decision_reason: str = ""


class ToolApprovalManager:
    """Manages approvals for sensitive actions (e.g. database deletes, cloud provisioning)."""

    CRITICAL_TOOLS = {"delete_database", "execute_sql_migration", "transfer_funds", "shutdown_instance"}

    def __init__(self, approval_timeout_seconds: float = 60.0):
        self.pending_requests: Dict[str, ToolExecutionRequest] = {}
        self.audit_log: List[ToolExecutionRequest] = []
        self.timeout = approval_timeout_seconds

    def requires_approval(self, tool_name: str) -> bool:
        """Determines if the tool requires explicit human approval."""
        return tool_name in self.CRITICAL_TOOLS

    def create_request(self, tool_name: str, arguments: Dict[str, Any]) -> ToolExecutionRequest:
        """Submit an action for human review."""
        req_id = f"appr_{uuid.uuid4().hex[:8]}"
        req = ToolExecutionRequest(request_id=req_id, tool_name=tool_name, arguments=arguments)
        self.pending_requests[req_id] = req
        return req

    def decide(self, request_id: str, approved: bool, reason: str = "") -> ToolExecutionRequest:
        """Human reviewer decision."""
        if request_id not in self.pending_requests:
            raise KeyError(f"No pending request with id {request_id}")

        req = self.pending_requests.pop(request_id)
        if time.time() - req.created_at > self.timeout:
            req.status = ApprovalStatus.TIMED_OUT
            req.decision_reason = "Approval window expired"
        else:
            req.status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
            req.decision_reason = reason

        self.audit_log.append(req)
        return req


class AgentLoopGuard:
    """Safety guardrail limiting agent loop iterations and token budgets."""

    def __init__(self, max_iterations: int = 10, max_token_budget: int = 8000):
        self.max_iterations = max_iterations
        self.max_token_budget = max_token_budget
        self.current_iteration = 0
        self.accumulated_tokens = 0

    def step(self, tokens_used: int = 0) -> None:
        """Advance iteration counter and verify bounds."""
        self.current_iteration += 1
        self.accumulated_tokens += tokens_used

        if self.current_iteration > self.max_iterations:
            raise RuntimeError(
                f"Agent safety halt: Exceeded max allowed iterations ({self.max_iterations})"
            )

        if self.accumulated_tokens > self.max_token_budget:
            raise RuntimeError(
                f"Agent safety halt: Exceeded token budget ({self.accumulated_tokens} > {self.max_token_budget})"
            )

    def is_active(self) -> bool:
        return self.current_iteration < self.max_iterations and self.accumulated_tokens < self.max_token_budget


if __name__ == "__main__":
    mgr = ToolApprovalManager(approval_timeout_seconds=5.0)

    assert mgr.requires_approval("delete_database") is True
    assert mgr.requires_approval("search_web") is False

    req = mgr.create_request("delete_database", {"table": "customers"})
    assert req.status == ApprovalStatus.PENDING

    # Approve
    decided = mgr.decide(req.request_id, approved=True, reason="Verified admin consent")
    assert decided.status == ApprovalStatus.APPROVED

    # Loop guard
    guard = AgentLoopGuard(max_iterations=3, max_token_budget=1000)
    guard.step(200)
    guard.step(300)
    assert guard.is_active() is True
    guard.step(200)

    try:
        guard.step(100)
        assert False, "Should have raised iteration error"
    except RuntimeError as e:
        assert "Exceeded max allowed iterations" in str(e)

    print("Tool approval & agent loop guard tests passed successfully!")
