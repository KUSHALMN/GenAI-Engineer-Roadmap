"""
Day 10: Parallel Tool Execution
Implements concurrent tool invocation using thread pools, handles partial failures,
gathers results deterministically, and enforces global execution timeouts.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Callable
import time

class ParallelToolExecutor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def execute_parallel(self, calls: List[Dict[str, Any]], timeout: float = 3.0) -> List[Dict[str, Any]]:
        """
        Executes a list of tool calls in parallel.
        calls format: [{"tool_name": str, "func": Callable, "args": dict}]
        """
        results = [None] * len(calls)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_index = {
                executor.submit(c["func"], **c["args"]): idx
                for idx, c in enumerate(calls)
            }

            for future in as_completed(future_to_index, timeout=timeout):
                idx = future_to_index[future]
                call_info = calls[idx]
                try:
                    data = future.result()
                    results[idx] = {
                        "tool": call_info["tool_name"],
                        "success": True,
                        "data": data,
                        "error": None
                    }
                except Exception as e:
                    results[idx] = {
                        "tool": call_info["tool_name"],
                        "success": False,
                        "data": None,
                        "error": str(e)
                    }

        return results

if __name__ == "__main__":
    def search_news(topic: str):
        time.sleep(0.05)
        return f"News regarding {topic}"

    def search_wiki(topic: str):
        time.sleep(0.05)
        return f"Wikipedia page for {topic}"

    def failing_tool(topic: str):
        raise ConnectionError("Upstream service unavailable")

    calls = [
        {"tool_name": "search_news", "func": search_news, "args": {"topic": "AI"}},
        {"tool_name": "search_wiki", "func": search_wiki, "args": {"topic": "AI"}},
        {"tool_name": "failing_tool", "func": failing_tool, "args": {"topic": "AI"}}
    ]

    executor = ParallelToolExecutor(max_workers=3)
    start = time.time()
    res = executor.execute_parallel(calls)
    elapsed = time.time() - start

    assert len(res) == 3
    assert res[0]["success"] is True
    assert res[1]["success"] is True
    assert res[2]["success"] is False
    print(f"Parallel tool execution completed in {elapsed:.3f}s with partial failure handling.")
    print("Day 10 AI Parallel Tool Executor passed all tests.")
