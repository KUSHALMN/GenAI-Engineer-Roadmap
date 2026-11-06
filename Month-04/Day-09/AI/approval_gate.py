"""
Day 09: Human-in-the-Loop Approval Gates
Implements policy-based action risk assessment, approval ticket generation,
and pause/resume interruption workflows for sensitive operations.
"""

from typing import Dict, Any, Optional
import uuid
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"         # Auto-execute (read operations)
    MEDIUM = "MEDIUM"   # Notify user
    HIGH = "HIGH"       # Block until human approval token provided

class ApprovalGate:
    def __init__(self):
        self.pending_approvals: Dict[str, Dict[str, Any]] = {}

    def assess_risk(self, tool_name: str, args: Dict[str, Any]) -> RiskLevel:
        if tool_name in ["read_file", "search_docs", "get_metrics"]:
            return RiskLevel.LOW
        elif tool_name in ["create_file", "send_notification"]:
            return RiskLevel.MEDIUM
        elif tool_name in ["delete_database", "execute_sql_write", "transfer_funds"]:
            return RiskLevel.HIGH
        return RiskLevel.HIGH

    def submit_action(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        risk = self.assess_risk(tool_name, args)
        if risk == RiskLevel.LOW:
            return {"status": "APPROVED_AUTO", "ticket_id": None}
        
        ticket_id = f"appr_{uuid.uuid4().hex[:8]}"
        self.pending_approvals[ticket_id] = {
            "tool_name": tool_name,
            "args": args,
            "risk": risk.value,
            "status": "PENDING"
        }
        return {
            "status": "AWAITING_HUMAN_APPROVAL",
            "ticket_id": ticket_id,
            "risk": risk.value,
            "message": f"Action '{tool_name}' requires manual supervisor authorization."
        }

    def resolve_approval(self, ticket_id: str, approved: bool) -> bool:
        if ticket_id not in self.pending_approvals:
            return False
        self.pending_approvals[ticket_id]["status"] = "APPROVED" if approved else "REJECTED"
        return approved

if __name__ == "__main__":
    gate = ApprovalGate()

    # Low risk
    r1 = gate.submit_action("read_file", {"path": "/var/log/app.log"})
    assert r1["status"] == "APPROVED_AUTO"

    # High risk
    r2 = gate.submit_action("transfer_funds", {"amount": 50000, "to": "acct_889"})
    assert r2["status"] == "AWAITING_HUMAN_APPROVAL"
    ticket = r2["ticket_id"]

    # Approve
    approved = gate.resolve_approval(ticket, approved=True)
    assert approved is True
    print(f"Approval gate successfully enforced risk policy on ticket {ticket}")
    print("Day 09 AI Approval Gate passed all tests.")
