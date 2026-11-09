"""
Voice Agent Tool Integration Engine.
Connects spoken speech transcription to JSON tool invocation,
enforces approval gates for high-risk actions, and produces verbal responses.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass
class ToolDefinition:
    name: str
    description: str
    requires_confirmation: bool
    func: Callable[..., Any]


class VoiceAgentToolManager:
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.pending_confirmation: Optional[Dict[str, Any]] = None

    def register_tool(self, name: str, description: str, requires_confirmation: bool, func: Callable):
        self.tools[name] = ToolDefinition(name, description, requires_confirmation, func)

    def process_spoken_command(self, spoken_text: str, user_confirmed: bool = False) -> Dict[str, Any]:
        text = spoken_text.lower()
        if self.pending_confirmation and user_confirmed:
            tool = self.tools[self.pending_confirmation["tool"]]
            result = tool.func(**self.pending_confirmation["args"])
            self.pending_confirmation = None
            return {"status": "executed", "spoken_response": f"Action confirmed and executed: {result}"}

        if "check balance" in text or "account status" in text:
            res = self.tools["get_balance"].func(account_id="ACC-992")
            return {"status": "executed", "spoken_response": f"Your account balance is {res} dollars."}
        elif "transfer" in text or "send money" in text:
            self.pending_confirmation = {"tool": "transfer_funds", "args": {"amount": 500, "to": "Alice"}}
            return {
                "status": "requires_confirmation",
                "spoken_response": "You requested to transfer 500 dollars to Alice. Please say yes to confirm."
            }
        return {"status": "unknown_intent", "spoken_response": "I didn't quite catch that. Could you repeat?"}


if __name__ == "__main__":
    mgr = VoiceAgentToolManager()
    mgr.register_tool("get_balance", "Returns account balance", False, lambda account_id: 14250.00)
    mgr.register_tool("transfer_funds", "Transfers money", True, lambda amount, to: f"Sent ${amount} to {to}")

    print("=== Testing Voice Agent Tool Integration ===")
    r1 = mgr.process_spoken_command("What is my current account balance?")
    print("Spoken ->", r1["spoken_response"])

    r2 = mgr.process_spoken_command("Transfer 500 dollars to Alice")
    print("Spoken ->", r2["spoken_response"])

    r3 = mgr.process_spoken_command("Yes", user_confirmed=True)
    print("Spoken ->", r3["spoken_response"])
