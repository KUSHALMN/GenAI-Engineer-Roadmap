"""
ZeRO (Zero Redundancy Optimizer) Memory Partitioning:
Static FP16/FP32 Model State Breakdown (16 Bytes/param),
ZeRO-Stage 1 (Optimizer States), ZeRO-Stage 2 (Gradients),
and ZeRO-Stage 3 (Parameters) Cluster Scaling Simulation.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ModelParametersSpec:
    num_parameters_billions: float # e.g. 70.0 for 70B model

    @property
    def total_params(self) -> float:
        return self.num_parameters_billions * 1e9


class ZeroMemoryPartitioner:
    """
    Simulates memory footprints per GPU across standard DDP vs ZeRO-1, ZeRO-2, and ZeRO-3.
    Assumes mixed-precision training:
    - FP16 model weights: 2 bytes / param
    - FP16 gradients: 2 bytes / param
    - FP32 master weights: 4 bytes / param
    - FP32 Adam momentum: 4 bytes / param
    - FP32 Adam variance: 4 bytes / param
    Total static state: 16 bytes per parameter.
    """
    def __init__(self, spec: ModelParametersSpec, num_gpus: int):
        self.spec = spec
        self.N_d = num_gpus

    def calculate_memory_gb(self) -> Dict[str, float]:
        N = self.spec.total_params
        GB = 1024 ** 3

        # Standard DDP: Each GPU replicates all 16 bytes/param
        standard_ddp_gb = (16.0 * N) / GB

        # ZeRO-Stage 1: Partitions Adam optimizer states (12 bytes/param) across N_d GPUs
        # Each GPU retains full weights (2B) + full gradients (2B) + partitioned opt state (12B / N_d)
        zero1_gb = (4.0 * N + (12.0 * N / self.N_d)) / GB

        # ZeRO-Stage 2: Partitions gradients (2B) and optimizer states (12B)
        # Each GPU retains full weights (2B) + partitioned grads (2B / N_d) + opt state (12B / N_d)
        zero2_gb = (2.0 * N + (14.0 * N / self.N_d)) / GB

        # ZeRO-Stage 3: Partitions all states linearly (16 bytes / N_d)
        zero3_gb = (16.0 * N / self.N_d) / GB

        return {
            "standard_ddp_gb": round(standard_ddp_gb, 2),
            "zero_stage_1_gb": round(zero1_gb, 2),
            "zero_stage_2_gb": round(zero2_gb, 2),
            "zero_stage_3_gb": round(zero3_gb, 2)
        }


if __name__ == "__main__":
    # Example: 13 Billion parameter model on 16 GPUs
    spec = ModelParametersSpec(num_parameters_billions=13.0)
    partitioner = ZeroMemoryPartitioner(spec, num_gpus=16)
    mem_report = partitioner.calculate_memory_gb()

    print("Memory Footprint for 13B Model on 16 GPUs (GB per GPU):")
    for k, v in mem_report.items():
        print(f" -> {k}: {v} GB")

    assert mem_report["standard_ddp_gb"] > 190.0 # ~193.7 GB (Impossible on single 80GB GPU)
    assert mem_report["zero_stage_3_gb"] < 15.0 # ~12.1 GB (Easily fits on an 80GB GPU!)
    assert mem_report["zero_stage_3_gb"] < mem_report["zero_stage_2_gb"] < mem_report["zero_stage_1_gb"]
    print("Day 06 ZeRO Memory Partitioner verification passed.")
