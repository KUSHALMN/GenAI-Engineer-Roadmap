# 🎯 Technical Interview Questions — Day 15: Distributed Checkpointing & Maximal Rectangle

## Question 1: How does PyTorch Distributed Checkpoint (DCP) eliminate the multi-minute GPU stall associated with legacy torch.save(model.state_dict())?
**Answer:**
1. **Legacy Bottleneck (Gather to Rank 0):** In traditional checkpointing, all model and optimizer states (often multiple terabytes for 70B+ models) must be All-Gathered across the network onto Rank 0, which then serializes the single massive file to disk. This causes severe GPU memory spikes (often triggering OOMs) and forces thousands of GPUs to sit completely idle for 10–20 minutes.
2. **Distributed Asynchronous Writing:**
   - DCP allows every GPU to write its own local tensor shards directly to parallel network storage (Lustre/GPFS/S3) in parallel without gathering.
   - Using asynchronous I/O threads, the write operation is delegated to a background CPU thread pool while the GPUs immediately resume forward compute for the next pretraining step.
   - Total GPU stall time drops from 15 minutes to $< 1$ second.

---

## Question 2: In LeetCode 85 (Maximal Rectangle), how is the 2D problem reduced to repeated 1D histogram calculations?
**Answer:**
- For each row $R_i$, consider that row as the ground baseline.
- An array `heights[C]` tracks the number of consecutive '1's ending at row $i$ for each column.
  - If `matrix[i][j] == '1'`, `heights[j] = heights[j] + 1`.
  - If `matrix[i][j] == '0'`, `heights[j] = 0` (breaks vertical continuity).
- Running LeetCode 84's monotonic stack algorithm on `heights` finds the maximum rectangle with base at row $i$ in $O(C)$ time.
- Processing all $R$ rows solves the entire problem in $O(R \times C)$ time and $O(C)$ space.
