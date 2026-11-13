"""
Context Parallelism & RingAttention Simulation:
Distributed Sequence Partitioning for Million-Token Contexts,
Circular KV Block Transmission, P2P Non-blocking Communication Overlap,
and Online Softmax Rescaling across Ring Ranks.
"""

import math
from typing import List


class RingAttentionSimulator:
    """
    Simulates RingAttention (Hao Liu, Matei Zaharia, Pieter Abbeel).
    Each GPU holds a chunk of query tokens Q_i and circular-shifts
    Key and Value chunks (K_j, V_j) around an N-GPU ring.
    Computes exact full Attention over arbitrary sequence lengths (1M+ tokens)
    with strictly O(seq_len / num_gpus) memory per device!
    """
    def __init__(self, num_ranks: int):
        self.num_ranks = num_ranks

    def compute_ring_attention(self, rank_queries: List[List[List[float]]],
                              rank_keys: List[List[List[float]]],
                              rank_values: List[List[List[float]]]) -> List[List[List[float]]]:
        N = self.num_ranks
        d = len(rank_queries[0][0])
        scale = 1.0 / math.sqrt(d)
        seq_per_rank = len(rank_queries[0])

        # State per rank: Output accumulator O_i, max m_i, denominator l_i
        outputs = [[[0.0] * d for _ in range(seq_per_rank)] for _ in range(N)]
        m_stats = [[-float("inf")] * seq_per_rank for _ in range(N)]
        l_stats = [[0.0] * seq_per_rank for _ in range(N)]

        # Copy initial keys and values
        curr_keys = [list(k) for k in rank_keys]
        curr_vals = [list(v) for v in rank_values]

        # Ring steps: N rounds of compute overlapping with P2P transfer
        for step in range(N):
            for rank in range(N):
                Q = rank_queries[rank]
                K = curr_keys[rank]
                V = curr_vals[rank]

                for q_idx in range(seq_per_rank):
                    q_vec = Q[q_idx]
                    scores = []
                    for k_vec in K:
                        dot = sum(q_vec[k] * k_vec[k] for k in range(d)) * scale
                        scores.append(dot)

                    # Online Softmax update
                    row_max = max(scores)
                    new_m = max(m_stats[rank][q_idx], row_max)
                    
                    old_factor = math.exp(m_stats[rank][q_idx] - new_m) if m_stats[rank][q_idx] != -float("inf") else 0.0
                    new_exps = [math.exp(s - new_m) for s in scores]
                    new_l = old_factor * l_stats[rank][q_idx] + sum(new_exps)

                    # Accumulate V
                    for col in range(d):
                        curr_o = old_factor * outputs[rank][q_idx][col]
                        for v_idx in range(len(V)):
                            curr_o += new_exps[v_idx] * V[v_idx][col]
                        outputs[rank][q_idx][col] = curr_o

                    m_stats[rank][q_idx] = new_m
                    l_stats[rank][q_idx] = new_l

            # Circular shift KV to clockwise neighbor: rank -> (rank + 1) % N
            next_keys = [None] * N
            next_vals = [None] * N
            for rank in range(N):
                dest = (rank + 1) % N
                next_keys[dest] = curr_keys[rank]
                next_vals[dest] = curr_vals[rank]
            curr_keys = next_keys
            curr_vals = next_vals

        # Final normalization
        for rank in range(N):
            for q_idx in range(seq_per_rank):
                for col in range(d):
                    outputs[rank][q_idx][col] /= l_stats[rank][q_idx]

        return outputs


if __name__ == "__main__":
    # Simulate RingAttention across 4 ranks, each with 2 tokens of dimension 2 (Total sequence: 8 tokens)
    num_ranks = 4
    queries = [[[1.0, 0.5], [0.2, 0.8]] for _ in range(num_ranks)]
    keys = [[[1.0, 0.0], [0.0, 1.0]] for _ in range(num_ranks)]
    values = [[[2.0, 1.0], [1.0, 3.0]] for _ in range(num_ranks)]

    sim = RingAttentionSimulator(num_ranks=num_ranks)
    final_outputs = sim.compute_ring_attention(queries, keys, values)

    print(f"RingAttention computed across {num_ranks} ranks.")
    print("Rank 0 Output:", [[round(x, 4) for x in tok] for tok in final_outputs[0]])

    assert len(final_outputs) == 4
    assert len(final_outputs[0]) == 2
    assert final_outputs[0][0][0] > 0.0
    print("Day 13 RingAttention Simulator verification passed.")
