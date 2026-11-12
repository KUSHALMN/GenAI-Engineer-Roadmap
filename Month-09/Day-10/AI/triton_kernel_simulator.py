"""
Triton GPU Custom Kernel Simulation:
Block Pointers, Grid Program IDs, Vector Masking,
and Fused Element-wise Operations (Add + LayerNorm + GELU).
"""

import math
from typing import List


class TritonFusedKernelSimulator:
    """
    Simulates the execution semantics of an OpenAI Triton custom kernel:
    - Block-level scheduling via program_id
    - Tiled memory loads with boundary masking
    - Kernel operator fusion (Fused Residual Add + RMSNorm)
    """
    def __init__(self, block_size: int = 128):
        self.block_size = block_size

    def fused_residual_rmsnorm(self, x: List[float], residual: List[float], weight: List[float], eps: float = 1e-5) -> List[float]:
        N = len(x)
        output = [0.0] * N

        # Calculate number of Triton program blocks (Grid dimension)
        num_blocks = (N + self.block_size - 1) // self.block_size

        # Simulate parallel execution of each block program_id
        for pid in range(num_blocks):
            # Compute block pointer offsets
            block_start = pid * self.block_size
            block_offsets = [block_start + i for i in range(self.block_size)]

            # Load with boundary masking (mask = offsets < N)
            masked_indices = [idx for idx in block_offsets if idx < N]

            # 1. Fused Residual Addition: acc = x + residual
            acc = [x[i] + residual[i] for i in masked_indices]

            # 2. RMSNorm across the block/vector: sqrt(mean(acc^2) + eps)
            sum_sq = sum(val * val for val in acc)
            rms = math.sqrt(sum_sq / len(acc) + eps)

            # 3. Scale by learnable weight and write to output
            for local_idx, global_idx in enumerate(masked_indices):
                output[global_idx] = (acc[local_idx] / rms) * weight[global_idx]

        return output


if __name__ == "__main__":
    size = 256
    x = [0.5] * size
    res = [0.5] * size
    w = [1.0] * size

    simulator = TritonFusedKernelSimulator(block_size=128)
    out = simulator.fused_residual_rmsnorm(x, res, w)

    print(f"Triton Fused Kernel processed {len(out)} elements.")
    print("Sample output values:", [round(v, 4) for v in out[:4]])

    assert len(out) == size
    assert abs(out[0] - 1.0) < 0.01 # (0.5 + 0.5) / RMS(1.0) * 1.0 ≈ 1.0
    print("Day 10 Triton Kernel Simulator verification passed.")
