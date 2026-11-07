"""
Day 20: Batching and Continuous Batching
Simulates static batching vs continuous (iteration-level) batching:
Shows how continuous batching eliminates GPU bubble waste by evicting completed
sequences and inserting newly arrived requests at every decoding iteration.
"""

from typing import List, Dict, Any

class ContinuousBatchScheduler:
    def __init__(self, max_batch_size: int = 4):
        self.max_batch_size = max_batch_size
        self.active_requests: List[Dict[str, Any]] = []
        self.completed_requests: List[Dict[str, Any]] = []

    def step_decoding_iteration(self, new_incoming: List[Dict[str, Any]]):
        # 1. Admit new requests up to max_batch_size
        while new_incoming and len(self.active_requests) < self.max_batch_size:
            req = new_incoming.pop(0)
            self.active_requests.append(req)

        # 2. Advance 1 decode token for each active request
        remaining = []
        for req in self.active_requests:
            req["tokens_generated"] += 1
            if req["tokens_generated"] >= req["target_tokens"]:
                self.completed_requests.append(req)
            else:
                remaining.append(req)
        self.active_requests = remaining

if __name__ == "__main__":
    scheduler = ContinuousBatchScheduler(max_batch_size=2)
    queue = [
        {"id": "R1", "tokens_generated": 0, "target_tokens": 2},
        {"id": "R2", "tokens_generated": 0, "target_tokens": 4},
        {"id": "R3", "tokens_generated": 0, "target_tokens": 1}
    ]

    # Iteration 1
    scheduler.step_decoding_iteration(queue)
    # Iteration 2 (R1 completes)
    scheduler.step_decoding_iteration(queue)
    assert len(scheduler.completed_requests) == 1 and scheduler.completed_requests[0]["id"] == "R1"

    # Iteration 3 (R3 was admitted immediately into vacated slot!)
    scheduler.step_decoding_iteration(queue)
    assert len(scheduler.completed_requests) >= 2 # R3 also completed
    print("Continuous Batching successfully admitted R3 into slot without waiting for R2.")
    print("Day 20 AI Continuous Batching Simulation passed all tests.")
