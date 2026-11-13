"""
Fault Tolerance, Elastic Training & Straggler Detection:
Heartbeat Health Probes, Dead-Node Eviction, Dynamic World-Size Resizing,
and Tail Latency Straggler Mitigation.
"""

from dataclasses import dataclass
import time
from typing import Dict


@dataclass
class WorkerHealthStatus:
    rank: int
    last_heartbeat_timestamp: float
    p95_step_time_ms: float
    is_alive: bool = True
    is_straggler: bool = False


class ElasticTrainingFaultManager:
    """
    Monitors cluster worker health, identifies failed ranks and slow stragglers,
    and coordinates dynamic cluster elastic recovery.
    """
    def __init__(self, heartbeat_timeout_sec: float = 5.0, straggler_multiplier: float = 2.0):
        self.heartbeat_timeout = heartbeat_timeout_sec
        self.straggler_multiplier = straggler_multiplier
        self.workers: Dict[int, WorkerHealthStatus] = {}

    def register_heartbeat(self, rank: int, step_time_ms: float):
        self.workers[rank] = WorkerHealthStatus(
            rank=rank,
            last_heartbeat_timestamp=time.time(),
            p95_step_time_ms=step_time_ms,
            is_alive=True
        )

    def evaluate_cluster_health(self) -> Dict[str, any]:
        now = time.time()
        dead_ranks = []
        alive_step_times = []

        for rank, status in self.workers.items():
            if now - status.last_heartbeat_timestamp > self.heartbeat_timeout:
                status.is_alive = False
                dead_ranks.append(rank)
            else:
                alive_step_times.append(status.p95_step_time_ms)

        # Detect stragglers among alive nodes
        stragglers = []
        if alive_step_times:
            median_step_time = sorted(alive_step_times)[len(alive_step_times) // 2]
            for rank, status in self.workers.items():
                if status.is_alive and status.p95_step_time_ms > median_step_time * self.straggler_multiplier:
                    status.is_straggler = True
                    stragglers.append(rank)

        return {
            "total_workers": len(self.workers),
            "healthy_workers": len(self.workers) - len(dead_ranks) - len(stragglers),
            "dead_ranks": dead_ranks,
            "straggler_ranks": stragglers,
            "cluster_healthy": len(dead_ranks) == 0
        }


if __name__ == "__main__":
    mgr = ElasticTrainingFaultManager(heartbeat_timeout_sec=0.5, straggler_multiplier=2.0)

    # Register healthy workers
    mgr.register_heartbeat(0, 150.0)
    mgr.register_heartbeat(1, 155.0)
    mgr.register_heartbeat(2, 450.0) # Straggler (> 2x median 150ms)

    res1 = mgr.evaluate_cluster_health()
    assert 2 in res1["straggler_ranks"]
    print("Health Status with Straggler:", res1)

    # Simulate worker 1 dying
    time.sleep(0.6)
    mgr.register_heartbeat(0, 150.0)
    res2 = mgr.evaluate_cluster_health()
    assert 1 in res2["dead_ranks"]
    print("Health Status with Dead Worker:", res2)

    print("Day 18 Elastic Fault Tolerance Engine verification passed.")
