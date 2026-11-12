# 🎯 Technical Interview Questions — Day 07: PyTorch FSDP & Segment Trees

## Question 1: How does PyTorch FSDP orchestrate layer-by-layer forward and backward execution to maintain low peak VRAM?
**Answer:**
1. **Sharded Parameter Storage:** During initialization, each Transformer layer's parameters are split evenly across all $N$ GPUs.
2. **Forward Pass Pre-fetch & Discard:**
   - Before executing layer $L_i$, FSDP triggers an asynchronous **All-Gather** to reconstruct the full unsharded parameters of $L_i$.
   - The forward pass computes activations using the full weights.
   - Immediately upon completion, FSDP discards the unsharded parameters, freeing memory before moving to layer $L_{i+1}$.
3. **Backward Pass Re-gather & Reduce-Scatter:**
   - During the backward pass (running in reverse order $L_n \dots L_1$), FSDP once again All-Gathers the full parameters for layer $L_i$ to compute input and parameter gradients.
   - Parameter gradients are immediately partitioned across ranks via **Reduce-Scatter**, freeing full gradients from local GPU memory.

---

## Question 2: Why does an array-based Segment Tree require up to 4N nodes for an array of size N?
**Answer:**
- A Segment Tree is a full binary tree. If $N$ is a power of 2, the number of leaf nodes is $N$, and internal nodes equal $N - 1$, totaling $2N - 1$ nodes.
- However, if $N$ is not a power of 2, the tree height is $\lceil \log_2 N \rceil + 1$. In the worst case (e.g. $N = 2^k + 1$), the lowest level is partially filled, requiring the tree capacity to match a complete binary tree of height $k + 2$.
- The number of nodes in such a tree is bounded strictly by $2^{\lceil \log_2 N \rceil + 1} - 1 < 4N$. Allocating an array of size $4N$ guarantees no index out-of-bounds without requiring dynamic node heap allocations.
