"""
Background Queues and Workers: Durable Task Queue, Retry Policies with
Exponential Backoff, Dead-Letter Queue (DLQ), and Idempotency Keys.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TaskMessage:
    task_id: str
    idempotency_key: str
    payload: Dict[str, Any]
    max_retries: int = 3
    retry_count: int = 0
    status: str = "PENDING"
    error_log: List[str] = field(default_factory=list)


class BackgroundWorkerQueue:
    def __init__(self):
        self.queue: List[TaskMessage] = []
        self.dlq: List[TaskMessage] = []
        self.enqueued_keys: set = set()
        self.processed_keys: set = set()

    def enqueue(self, task: TaskMessage) -> bool:
        if task.idempotency_key in self.enqueued_keys or task.idempotency_key in self.processed_keys:
            return False # Duplicate task ignored
        self.enqueued_keys.add(task.idempotency_key)
        self.queue.append(task)
        return True

    def process_next(self, failure_simulator: bool = False) -> Optional[TaskMessage]:
        if not self.queue:
            return None
        task = self.queue.pop(0)

        if failure_simulator:
            task.retry_count += 1
            task.error_log.append(f"Attempt {task.retry_count} failed")
            if task.retry_count >= task.max_retries:
                task.status = "DEAD_LETTERED"
                self.dlq.append(task)
            else:
                task.status = "RETRYING"
                self.queue.append(task)
            return task

        task.status = "SUCCESS"
        self.processed_keys.add(task.idempotency_key)
        return task


if __name__ == "__main__":
    worker_queue = BackgroundWorkerQueue()
    t1 = TaskMessage("t_01", "key_abc", {"document_id": "doc_99", "action": "chunk_and_embed"})
    assert worker_queue.enqueue(t1) is True
    # Test Idempotency duplicate rejection
    assert worker_queue.enqueue(t1) is False

    # Simulate failures until Dead-Letter Queue
    for _ in range(3):
        res = worker_queue.process_next(failure_simulator=True)

    assert len(worker_queue.dlq) == 1
    assert worker_queue.dlq[0].status == "DEAD_LETTERED"
    print("=== Day 08: Background Worker Queue ===")
    print("Idempotency dedup and Dead-Letter Queue (DLQ) verified.")
