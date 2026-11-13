# 📝 Notes — Day 12: Sequence Parallelism & Hierholzer's Algorithm

- **Megatron-SP vs DeepSpeed-Ulysses:** Megatron-SP shards along sequence dimension for LayerNorm/Dropout and uses All-Gather/Reduce-Scatter around Attention. DeepSpeed-Ulysses shards sequence across Attention heads using All-to-All communication.
- **Eulerian Path Criteria:** A directed graph has an Eulerian path if at most one vertex has $\text{out} - \text{in} = 1$ (start), at most one has $\text{in} - \text{out} = 1$ (end), and all other vertices have $\text{in} = \text{out}$.
