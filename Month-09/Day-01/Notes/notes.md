# 📝 Notes — Day 01: BPE Tokenizers & 0/1 Knapsack DP

- **BPE Merge Table:** Deterministic lookup table of byte tuples mapped to integer IDs; merges must be evaluated in strict training-order priority during inference.
- **Partition Equal Subset Sum:** Reduces to 0/1 Knapsack with target sum $\text{TotalSum} / 2$. If sum is odd, partition is immediately impossible.
- **Memory Footprint:** 1D array of size `target + 1` consumes $O(\text{Target})$ space instead of $O(N \times \text{Target})$ 2D matrix allocations.
