"""
Load Balancing and Autoscaling: Round-Robin, Least Connections,
Queue Depth Metrics, and GPU Instance Autoscaling Logic.
"""

from dataclasses import dataclass
import math
from typing import List


@dataclass
class InferenceWorkerNode:
    node_id: str
    active_requests: int
    is_healthy: bool = True


class LoadBalancerAutoscaler:
    def __init__(self, target_concurrency_per_node: int = 4):
        self.nodes: List[InferenceWorkerNode] = []
        self.target_concurrency = target_concurrency_per_node

    def add_node(self, node: InferenceWorkerNode):
        self.nodes.append(node)

    def route_least_connections(self) -> InferenceWorkerNode:
        healthy_nodes = [n for n in self.nodes if n.is_healthy]
        if not healthy_nodes:
            raise RuntimeError("No healthy inference nodes available!")
        # Select node with minimum active requests
        chosen = min(healthy_nodes, key=lambda n: n.active_requests)
        chosen.active_requests += 1
        return chosen

    def calculate_desired_replicas(self, pending_queue_depth: int) -> int:
        total_in_flight = sum(n.active_requests for n in self.nodes if n.is_healthy) + pending_queue_depth
        desired = math.ceil(total_in_flight / self.target_concurrency)
        return max(1, desired)


if __name__ == "__main__":
    lb = LoadBalancerAutoscaler(target_concurrency_per_node=4)
    n1 = InferenceWorkerNode("gpu-worker-1", active_requests=3)
    n2 = InferenceWorkerNode("gpu-worker-2", active_requests=1)
    lb.add_node(n1)
    lb.add_node(n2)

    selected = lb.route_least_connections()
    assert selected.node_id == "gpu-worker-2"

    # Autoscaling calculation: 16 pending requests -> needs 5 nodes
    replicas = lb.calculate_desired_replicas(pending_queue_depth=16)
    assert replicas >= 5
    print("=== Day 17: Load Balancer & Autoscaler ===")
    print(f"Least connections selected: {selected.node_id} | Desired Replicas: {replicas}")
