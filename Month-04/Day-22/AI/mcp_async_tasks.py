"""
Day 22: MCP Long-Running Tasks and Notifications
Manages asynchronous background tool tasks, progress updates,
cancellation tokens, and polling mechanics.
"""

from typing import Dict, Any, Optional
import uuid
import time
from enum import Enum

class TaskStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

class AsyncTaskManager:
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def start_task(self, tool_name: str, args: Dict[str, Any]) -> str:
        task_id = f"task_{uuid.uuid4().hex[:6]}"
        self.tasks[task_id] = {
            "task_id": task_id,
            "tool_name": tool_name,
            "status": TaskStatus.QUEUED,
            "progress": 0,
            "result": None,
            "cancelled": False
        }
        return task_id

    def update_progress(self, task_id: str, progress_pct: int):
        if task_id in self.tasks:
            t = self.tasks[task_id]
            if not t["cancelled"]:
                t["status"] = TaskStatus.RUNNING
                t["progress"] = progress_pct
                if progress_pct >= 100:
                    t["status"] = TaskStatus.COMPLETED
                    t["result"] = f"Task {task_id} completed successfully."

    def cancel_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            t = self.tasks[task_id]
            if t["status"] in [TaskStatus.QUEUED, TaskStatus.RUNNING]:
                t["cancelled"] = True
                t["status"] = TaskStatus.CANCELLED
                return True
        return False

    def poll_task(self, task_id: str) -> Dict[str, Any]:
        return self.tasks.get(task_id, {"status": "NOT_FOUND"})

if __name__ == "__main__":
    mgr = AsyncTaskManager()
    tid = mgr.start_task("train_custom_model", {"epochs": 10})
    assert mgr.poll_task(tid)["status"] == TaskStatus.QUEUED

    mgr.update_progress(tid, 50)
    assert mgr.poll_task(tid)["status"] == TaskStatus.RUNNING
    assert mgr.poll_task(tid)["progress"] == 50

    mgr.update_progress(tid, 100)
    assert mgr.poll_task(tid)["status"] == TaskStatus.COMPLETED
    print(f"Task status after completion: {mgr.poll_task(tid)}")

    # Cancellation test
    tid2 = mgr.start_task("large_export", {})
    cancelled = mgr.cancel_task(tid2)
    assert cancelled is True
    assert mgr.poll_task(tid2)["status"] == TaskStatus.CANCELLED
    print("Day 22 AI MCP Async Tasks passed all tests.")
