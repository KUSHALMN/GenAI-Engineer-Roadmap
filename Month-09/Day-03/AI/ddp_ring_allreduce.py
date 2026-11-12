"""
Distributed Data Parallelism (DDP) Ring All-Reduce Simulation:
Scatter-Reduce Phase, All-Gather Phase, Communication Volume Bounds,
and Gradient Bucketing Overlap.
"""

from typing import List


class RingAllReduceSimulator:
    """
    Simulates NCCL Ring All-Reduce across N virtual GPU ranks.
    Communication volume per worker is exactly 2 * ((N - 1) / N) * S bytes,
    completely independent of world size!
    """
    def __init__(self, world_size: int):
        self.world_size = world_size

    def all_reduce(self, rank_tensors: List[List[float]]) -> List[List[float]]:
        N = self.world_size
        chunk_size = len(rank_tensors[0]) // N
        assert chunk_size * N == len(rank_tensors[0]), "Tensor size must be divisible by world size"

        # Split each rank's tensor into N equal chunks
        buffers = []
        for t in rank_tensors:
            buffers.append([t[i * chunk_size:(i + 1) * chunk_size] for i in range(N)])

        # 1. Scatter-Reduce Phase (N - 1 steps)
        for step in range(N - 1):
            for rank in range(N):
                send_chunk_idx = (rank - step) % N
                recv_rank = (rank + 1) % N
                
                # Send chunk from rank to recv_rank and accumulate
                for i in range(chunk_size):
                    buffers[recv_rank][send_chunk_idx][i] += buffers[rank][send_chunk_idx][i]

        # 2. All-Gather Phase (N - 1 steps)
        for step in range(N - 1):
            for rank in range(N):
                send_chunk_idx = (rank - step + 1) % N
                recv_rank = (rank + 1) % N
                buffers[recv_rank][send_chunk_idx] = list(buffers[rank][send_chunk_idx])

        # Flatten back into complete reduced tensors
        reduced = []
        for rank in range(N):
            flat = [val for chunk in buffers[rank] for val in chunk]
            reduced.append(flat)
        return reduced


if __name__ == "__main__":
    world_size = 4
    # Each rank has 4 parameters
    rank_gradients = [
        [1.0, 2.0, 3.0, 4.0], # Rank 0
        [2.0, 1.0, 0.0, 1.0], # Rank 1
        [0.0, 3.0, 1.0, 2.0], # Rank 2
        [1.0, 0.0, 2.0, 1.0]  # Rank 3
    ]

    simulator = RingAllReduceSimulator(world_size)
    results = simulator.all_reduce(rank_gradients)

    expected_sum = [4.0, 6.0, 6.0, 8.0]
    print("Ring All-Reduce Output for Rank 0:", results[0])
    for rank in range(world_size):
        assert results[rank] == expected_sum, f"Rank {rank} did not match expected reduction"

    print("Day 03 DDP Ring All-Reduce verification passed.")
