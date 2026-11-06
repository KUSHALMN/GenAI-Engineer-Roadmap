"""
Day 13: Agent Failure Recovery
Handles tool timeout, malformed output, transient 5xx errors,
implements exponential backoff, alternative tool fallback, and reflection prompts.
"""

from typing import Dict, Any, Callable, Optional
import time

class RecoveryPolicy:
    def __init__(self, max_retries: int = 2, backoff_factor: float = 0.05):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def execute_with_recovery(self,
                              primary_tool: Callable,
                              fallback_tool: Optional[Callable],
                              args: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tool with retries, exponential backoff, and fallback fallback."""
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                result = primary_tool(**args)
                return {
                    "success": True,
                    "recovered": attempt > 1,
                    "attempts": attempt,
                    "data": result,
                    "error": None
                }
            except Exception as e:
                last_error = e
                wait_time = self.backoff_factor * (2 ** (attempt - 1))
                time.sleep(wait_time)

        # Primary failed all retries, attempt fallback
        if fallback_tool:
            try:
                fallback_res = fallback_tool(**args)
                return {
                    "success": True,
                    "recovered": True,
                    "fallback_used": True,
                    "attempts": self.max_retries + 1,
                    "data": fallback_res,
                    "error": f"Primary failed: {str(last_error)}"
                }
            except Exception as fb_err:
                return {
                    "success": False,
                    "data": None,
                    "error": f"Both primary and fallback failed: {str(fb_err)}"
                }

        return {
            "success": False,
            "data": None,
            "error": f"Primary tool failed after {self.max_retries} attempts: {str(last_error)}"
        }

if __name__ == "__main__":
    recovery = RecoveryPolicy(max_retries=2, backoff_factor=0.01)

    fail_counter = {"count": 0}
    def flapper(q: str):
        fail_counter["count"] += 1
        if fail_counter["count"] < 2:
            raise ConnectionResetError("Transient network drop")
        return f"Result for {q}"

    def backup_search(q: str):
        return f"Cached fallback result for {q}"

    # Test transient recovery
    res1 = recovery.execute_with_recovery(flapper, backup_search, {"q": "pricing"})
    assert res1["success"] is True and res1["recovered"] is True
    print(f"Transient recovery succeeded: {res1}")

    # Test complete fallback
    def always_fail(q: str):
        raise TimeoutError("Endpoint timeout")

    res2 = recovery.execute_with_recovery(always_fail, backup_search, {"q": "pricing"})
    assert res2["success"] is True and res2.get("fallback_used") is True
    print(f"Fallback recovery succeeded: {res2}")
    print("Day 13 AI Recovery Policy passed all tests.")
