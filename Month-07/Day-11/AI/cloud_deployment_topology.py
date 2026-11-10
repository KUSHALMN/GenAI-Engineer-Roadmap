"""
Cloud Deployment Concepts: Multi-AZ High Availability Topology,
Managed DB Replication, Private Subnet Routing, and Egress Cost Estimator.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ComputeInstance:
    instance_type: str
    vcpus: int
    gpu_type: str
    hourly_rate_usd: float
    az: str


class CloudTopologyPlanner:
    def __init__(self):
        self.pricing: Dict[str, float] = {
            "g5.2xlarge": 1.212,   # 1x A10G (24GB)
            "p4d.24xlarge": 32.77, # 8x A100 (40GB)
            "c6i.2xlarge": 0.34    # CPU worker
        }

    def estimate_monthly_cost(self, instances: List[ComputeInstance], storage_gb: int, egress_gb: int) -> Dict[str, float]:
        hours_per_month = 730
        compute_cost = sum(inst.hourly_rate_usd * hours_per_month for inst in instances)
        storage_cost = storage_gb * 0.08 # Multi-AZ gp3
        egress_cost = egress_gb * 0.09   # AWS internet egress
        total = compute_cost + storage_cost + egress_cost
        return {
            "compute_cost_usd": round(compute_cost, 2),
            "storage_cost_usd": round(storage_cost, 2),
            "egress_cost_usd": round(egress_cost, 2),
            "total_monthly_usd": round(total, 2)
        }


if __name__ == "__main__":
    planner = CloudTopologyPlanner()
    cluster = [
        ComputeInstance("g5.2xlarge", 8, "NVIDIA A10G", 1.212, "us-east-1a"),
        ComputeInstance("g5.2xlarge", 8, "NVIDIA A10G", 1.212, "us-east-1b"),
        ComputeInstance("c6i.2xlarge", 8, "None", 0.34, "us-east-1a")
    ]
    budget = planner.estimate_monthly_cost(cluster, storage_gb=500, egress_gb=2000)
    assert budget["total_monthly_usd"] > 2000.0
    print("=== Day 11: Cloud Topology & Cost Estimator ===")
    print(f"Total Monthly Cluster Budget: ${budget['total_monthly_usd']}")
