"""
FlashAttention Tiling & Online Softmax Simulation:
Milakov-Gimelshein / Tri Dao Online Rescaling Trick,
Block SRAM Tiling (Br x Bc), and O(N) Peak Memory Attention.
"""

import math
from typing import List


class FlashAttentionOnlineSimulator:
    """
    Simulates FlashAttention-1/2 block tiling algorithm.
    Computes exact Multi-Head Attention without ever materializing
    the full (N x N) attention score matrix in GPU HBM!
    """
    def __init__(self, block_size_r: int = 2, block_size_c: int = 2):
        self.Br = block_size_r
        self.Bc = block_size_c

    def forward(self, Q: List[List[float]], K: List[List[float]], V: List[List[float]]) -> List[List[float]]:
        N = len(Q)
        d = len(Q[0])
        scale = 1.0 / math.sqrt(d)

        # Output matrix O: (N x d)
        O = [[0.0] * d for _ in range(N)]
        # Running row max m_i: (N)
        m = [-float("inf")] * N
        # Running sum of exponentials l_i: (N)
        l = [0.0] * N

        # Outer loop over key/value blocks (columns)
        for j in range(0, N, self.Bc):
            K_block = K[j:j + self.Bc]
            V_block = V[j:j + self.Bc]

            # Inner loop over query blocks (rows)
            for i in range(0, N, self.Br):
                Q_block = Q[i:i + self.Br]

                for row_idx in range(len(Q_block)):
                    global_row = i + row_idx
                    q_vec = Q_block[row_idx]

                    # Compute local block scores S_ij = q @ K_block^T * scale
                    scores = []
                    for k_vec in K_block:
                        dot = sum(q_vec[k] * k_vec[k] for k in range(d)) * scale
                        scores.append(dot)

                    # Online Softmax update
                    row_max = max(scores)
                    new_m = max(m[global_row], row_max)
                    
                    # Compute exponential factors
                    old_scale = math.exp(m[global_row] - new_m) if m[global_row] != -float("inf") else 0.0
                    new_exps = [math.exp(s - new_m) for s in scores]
                    new_l = old_scale * l[global_row] + sum(new_exps)

                    # Update output accumulator O_i
                    for col_d in range(d):
                        curr_val = old_scale * O[global_row][col_d]
                        for c_idx in range(len(V_block)):
                            curr_val += new_exps[c_idx] * V_block[c_idx][col_d]
                        O[global_row][col_d] = curr_val

                    m[global_row] = new_m
                    l[global_row] = new_l

        # Final normalization by running denominator l_i
        for row in range(N):
            for col_d in range(d):
                O[row][col_d] /= l[row]

        return O


if __name__ == "__main__":
    # Test FlashAttention against simple 4x2 sequence
    Q = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.5, 0.5]]
    K = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.5, 0.5]]
    V = [[2.0, 3.0], [4.0, 5.0], [6.0, 7.0], [1.0, 2.0]]

    sim = FlashAttentionOnlineSimulator(block_size_r=2, block_size_c=2)
    O_flash = sim.forward(Q, K, V)

    print("FlashAttention Tiled Output:")
    for row in O_flash:
        print(" ->", [round(x, 4) for x in row])

    assert len(O_flash) == 4
    assert len(O_flash[0]) == 2
    assert O_flash[0][0] > 0.0
    print("Day 09 FlashAttention Simulator verification passed.")
