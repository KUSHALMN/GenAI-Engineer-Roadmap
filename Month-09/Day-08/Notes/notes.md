# 📝 Notes — Day 08: 3D Parallelism Grid & Kahn's Algorithm

- **Cartesian Process Groups:** PyTorch `torch.distributed.new_group` initializes disjoint communicator communicators for each slice of the 3D grid.
- **Kahn's Queue vs DFS:** Kahn's algorithm operates iteratively with an explicit queue, eliminating JVM/call-stack overflow risks on massive DAGs with $10^6$ nodes.
