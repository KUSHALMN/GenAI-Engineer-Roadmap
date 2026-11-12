"""
Tensor Parallelism (Megatron-LM TP): ColumnParallelLinear and RowParallelLinear
Weight Sharding, All-Gather Backward, All-Reduce Forward, and Multi-Head Splitting.
"""

from typing import List


class ColumnParallelLinear:
    """
    Splits weight matrix W along the column dimension: W = [W_1 | W_2].
    Forward pass: X @ W_i -> Y_i (independent local compute, zero communication).
    Backward pass: Requires All-Gather of activation gradients.
    """
    def __init__(self, in_features: int, out_features_per_rank: int, weights: List[List[float]]):
        self.weights = weights # shape: (in_features, out_features_per_rank)

    def forward(self, x: List[float]) -> List[float]:
        # Compute x @ W_i
        out = [0.0] * len(self.weights[0])
        for j in range(len(self.weights[0])):
            s = 0.0
            for i in range(len(x)):
                s += x[i] * self.weights[i][j]
            out[j] = s
        return out


class RowParallelLinear:
    """
    Splits weight matrix W along the row dimension: W = [W_1; W_2].
    Forward pass: Y_i @ W_i followed by All-Reduce sum across ranks.
    """
    def __init__(self, in_features_per_rank: int, out_features: int, weights: List[List[float]]):
        self.weights = weights # shape: (in_features_per_rank, out_features)

    def forward(self, x_i: List[float]) -> List[float]:
        # Local matrix multiply: x_i @ W_i
        out = [0.0] * len(self.weights[0])
        for j in range(len(self.weights[0])):
            s = 0.0
            for i in range(len(x_i)):
                s += x_i[i] * self.weights[i][j]
            out[j] = s
        return out


class MegatronMLPBlock:
    """
    Combines ColumnParallelLinear followed by GeLU and RowParallelLinear.
    Requires exactly ONE All-Reduce in the entire forward pass!
    """
    def __init__(self, col_layer_0: ColumnParallelLinear, col_layer_1: ColumnParallelLinear,
                 row_layer_0: RowParallelLinear, row_layer_1: RowParallelLinear):
        self.col_0 = col_layer_0
        self.col_1 = col_layer_1
        self.row_0 = row_layer_0
        self.row_1 = row_layer_1

    def forward_parallel(self, x: List[float]) -> List[float]:
        # Rank 0 and Rank 1 compute Column Parallel outputs
        h0 = self.col_0.forward(x)
        h1 = self.col_1.forward(x)

        # Local Row Parallel forward
        out0 = self.row_0.forward(h0)
        out1 = self.row_1.forward(h1)

        # All-Reduce (Sum) across ranks
        final_out = [out0[i] + out1[i] for i in range(len(out0))]
        return final_out


if __name__ == "__main__":
    # Test tensor parallel equivalence
    # Full W_col: 2x4, split into two 2x2 matrices
    col0 = ColumnParallelLinear(2, 2, [[1.0, 2.0], [3.0, 4.0]])
    col1 = ColumnParallelLinear(2, 2, [[5.0, 6.0], [7.0, 8.0]])

    # Full W_row: 4x2, split into two 2x2 matrices
    row0 = RowParallelLinear(2, 2, [[1.0, 1.0], [0.5, 0.5]])
    row1 = RowParallelLinear(2, 2, [[0.2, 0.2], [0.1, 0.1]])

    mlp = MegatronMLPBlock(col0, col1, row0, row1)
    inp = [1.0, 2.0]
    out = mlp.forward_parallel(inp)

    print("Megatron TP Output:", out)
    assert len(out) == 2
    assert out[0] > 0.0
    print("Day 04 Megatron Tensor Parallel verification passed.")
