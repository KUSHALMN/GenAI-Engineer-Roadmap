# 🎯 Technical Interview Questions — Day 04: Megatron Tensor Parallel & Prim's MST

## Question 1: How does Megatron-LM design the Transformer MLP and Multi-Head Attention blocks to require only two All-Reduce operations per Transformer layer?
**Answer:**
1. **Self-Attention Block:**
   - **Column Parallel:** The query ($Q$), key ($K$), and value ($V$) projection weights are column-partitioned across the attention heads. Each GPU computes its local multi-head attention scores independently with zero inter-GPU communication.
   - **Row Parallel:** The output projection matrix ($W_O$) is row-partitioned. Multiplying local attention outputs with $W_O$ produces partial output vectors, which require a single **All-Reduce (Sum)** to synchronize before adding the residual connection.
2. **MLP Block:**
   - **Column Parallel:** The first linear layer ($h = \text{GELU}(X W_{\text{in}})$) is column-partitioned. The non-linear activation GELU applies element-wise to each GPU's local partition with zero communication.
   - **Row Parallel:** The second linear layer ($Y = h W_{\text{out}}$) is row-partitioned. Its output requires a single **All-Reduce (Sum)** before the final residual addition.
3. **Total Overhead:** Exactly 2 All-Reduce calls in the forward pass and 2 in the backward pass per layer, strictly bound to high-bandwidth NVLink intra-node fabrics.

---

## Question 2: In Prim's Algorithm, what is the "Cut Property" that guarantees greedy edge selection produces an optimal MST?
**Answer:**
- **The Cut Property:** For any cut $C = (S, V \setminus S)$ in a connected undirected graph, if an edge $e = (u, v)$ crossing the cut has the strictly minimum weight among all crossing edges, then that edge must belong to every Minimum Spanning Tree.
- **Prim's Invariant:** At each step, Prim's algorithm maintains a cut where $S$ is the set of vertices already in the growing tree, and $V \setminus S$ are the unvisited vertices. By greedily selecting the minimum weight edge crossing this boundary via a min-heap, the cut property guarantees optimal substructure without backtracking.
