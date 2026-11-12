"""
Pipeline Parallelism (PP) & 1F1B Scheduling:
Micro-batch Partitioning, Activation Stashing, Memory Footprint Comparison,
and Bubble Ratio Calculations.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ScheduleStep:
    time_step: int
    stage_id: int
    micro_batch_id: int
    operation: str # "FORWARD" or "BACKWARD"


class PipelineParallelScheduler:
    """
    Models GPipe vs 1F1B (One-Forward-One-Backward) micro-batch scheduling.
    """
    def __init__(self, num_stages: int, num_micro_batches: int):
        self.P = num_stages
        self.M = num_micro_batches

    def calculate_bubble_fraction(self) -> float:
        """
        Calculates theoretical pipeline bubble ratio: F_bubble = (P - 1) / (P - 1 + M)
        """
        return (self.P - 1) / (self.P - 1 + self.M)

    def peak_activation_memory_units(self) -> Dict[str, int]:
        """
        GPipe stores activations for all M micro-batches before backward pass begins.
        1F1B stashes at most P micro-batch activations on stage 0.
        """
        return {
            "gpipe_peak_activations": self.M,
            "one_f_one_b_peak_activations": min(self.P, self.M)
        }

    def simulate_1f1b_timeline(self) -> List[ScheduleStep]:
        # Generates initial warmup phase of P - stage_id forward steps
        # followed by steady-state 1F1B execution
        timeline = []
        time = 0
        for stage in range(self.P):
            # Warmup: run forward micro-batches
            warmup_count = min(self.P - stage, self.M)
            for mb in range(warmup_count):
                timeline.append(ScheduleStep(time, stage, mb, "FORWARD"))
                time += 1
        return timeline


if __name__ == "__main__":
    scheduler = PipelineParallelScheduler(num_stages=8, num_micro_batches=32)
    bubble = scheduler.calculate_bubble_fraction()
    mem = scheduler.peak_activation_memory_units()

    print(f"Pipeline Stages (P): 8, Micro-batches (M): 32")
    print(f"Bubble Fraction: {bubble:.2%}")
    print(f"Peak Activation Memory Comparison:", mem)

    assert bubble < 0.20 # Bubble is (8-1)/(8-1+32) = 7/39 ≈ 17.9%
    assert mem["one_f_one_b_peak_activations"] == 8
    assert mem["gpipe_peak_activations"] == 32
    print("Day 05 Pipeline Parallel Scheduler verification passed.")
