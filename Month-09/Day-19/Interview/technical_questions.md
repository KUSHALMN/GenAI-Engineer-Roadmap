# 🎯 Technical Interview Questions — Day 19: MFU Profiling & N-Queens

## Question 1: What is the exact difference between Model FLOPs Utilization (MFU) and Hardware FLOPs Utilization (HFU)?
**Answer:**
1. **Model FLOPs Utilization (MFU):**
   - Measures the ratio of **pure algorithmic FLOPs** (theoretical forward + backward operations required by the architecture: $6P + 12LHS$ per token) to the theoretical maximum peak FLOP/s of the hardware cluster.
   - Ignores implementation-specific overheads like Activation Checkpointing recomputation. MFU directly reflects true pretraining efficiency ($45\text{--}55\%$ is considered state-of-the-art on H100 clusters).
2. **Hardware FLOPs Utilization (HFU):**
   - Measures the ratio of **total executed FLOPs** (including recomputed forward passes in activation checkpointing) to peak hardware capability.
   - HFU is always higher than MFU (typically $\text{HFU} \approx \frac{4}{3} \text{MFU}$ when full activation checkpointing is enabled).

---

## Question 2: In N-Queens II, how does bit manipulation optimize state checks to O(1) operations?
**Answer:**
- Standard backtracking maintains boolean arrays or sets for columns and diagonals, incurring array indexing and branching overhead.
- **Bitmask Representation:**
  - `cols`: Bit $c$ is 1 if column $c$ is attacked.
  - `diag1`: Tracks main diagonals ($r - c$). Advancing to row $r+1$ shifts the mask left (`(diag1 | p) << 1`).
  - `diag2`: Tracks anti-diagonals ($r + c$). Advancing shifts the mask right (`(diag2 | p) >> 1`).
- `available = ((1 << n) - 1) & ~(cols | diag1 | diag2)` isolates all valid positions in a single bitwise instruction.
- The lowest set bit extraction `p = available & (-available)` and clearing `available &= available - 1` eliminates iterating over invalid columns, achieving a $10\times$ speedup over array-based backtracking.
