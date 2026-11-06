"""
Day 12: Agent Stopping and Budget Policies
Enforces step counts, token limits, execution wall-clock budgets,
and loop detection via action/state hashing to stop runaway agents.
"""

from typing import Dict, Any, List, Set
import hashlib
import time

class BudgetPolicy:
    def __init__(self, max_steps: int = 10, max_tokens: int = 4000, max_seconds: float = 5.0, loop_threshold: int = 2):
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.max_seconds = max_seconds
        self.loop_threshold = loop_threshold

        self.current_steps = 0
        self.consumed_tokens = 0
        self.start_time = time.time()
        self.action_history: List[str] = []

    def record_step(self, tool_name: str, args: Dict[str, Any], tokens_used: int = 100):
        self.current_steps += 1
        self.consumed_tokens += tokens_used
        # Compute signature of action
        call_str = f"{tool_name}:{sorted(args.items())}"
        call_hash = hashlib.sha256(call_str.encode()).hexdigest()[:12]
        self.action_history.append(call_hash)

    def check_budget(self) -> Dict[str, Any]:
        """Returns whether execution is permitted or stopped due to policy limit."""
        if self.current_steps >= self.max_steps:
            return {"allowed": False, "reason": "MAX_STEPS_EXCEEDED"}

        if self.consumed_tokens >= self.max_tokens:
            return {"allowed": False, "reason": "TOKEN_BUDGET_EXCEEDED"}

        if time.time() - self.start_time >= self.max_seconds:
            return {"allowed": False, "reason": "WALL_CLOCK_TIMEOUT"}

        # Loop detection (same action called consecutive times)
        if len(self.action_history) >= self.loop_threshold:
            recent = self.action_history[-self.loop_threshold:]
            if len(set(recent)) == 1:
                return {"allowed": False, "reason": "REPETITIVE_LOOP_DETECTED"}

        return {"allowed": True, "reason": "WITHIN_BUDGET"}

if __name__ == "__main__":
    policy = BudgetPolicy(max_steps=5, max_tokens=1000, loop_threshold=2)

    # Normal step
    policy.record_step("search", {"q": "python"}, 150)
    assert policy.check_budget()["allowed"] is True

    # Same step again -> Loop detection trigger!
    policy.record_step("search", {"q": "python"}, 150)
    status = policy.check_budget()
    assert status["allowed"] is False
    assert status["reason"] == "REPETITIVE_LOOP_DETECTED"
    print(f"Policy successfully halted loop: {status}")
    print("Day 12 AI Budget Policy passed all tests.")
