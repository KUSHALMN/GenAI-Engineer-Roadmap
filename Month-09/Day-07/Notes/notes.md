# 📝 Notes — Day 07: FSDP & Segment Trees

- **Activation Checkpointing Overhead:** Recomputing forward passes during backward adds exactly $1 \times \text{Forward Time} \approx 33\%$ to total step compute time, but often allows doubling micro-batch size.
- **Segment Tree Indices:** For node $p$, left child is $2p + 1$ and right child is $2p + 2$ in 0-based indexing.
