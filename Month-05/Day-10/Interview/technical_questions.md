# Day 10: Technical Interview Preparation — Training Loop Checkpoints & LFU Cache

### Q1: Why is Gradient Accumulation mathematically equivalent to a larger batch size?
**Answer:**
By accumulating the loss gradients over $K$ forward and backward passes before calling `optimizer.step()`, the accumulated gradient is $\sum_{i=1}^K \nabla \mathcal{L}_i$. Dividing by $K$ calculates the exact average gradient of a batch of size $K \times \text{micro\_batch\_size}$, enabling training with large effective batch sizes without exceeding GPU VRAM.

### Q2: How does LFU Cache resolve ties when multiple keys have the identical minimum frequency?
**Answer:**
Ties among keys sharing the same minimum frequency are broken using LRU (Least Recently Used) order. In Java, mapping each frequency to a `LinkedHashSet` preserves insertion/access order so `.iterator().next()` retrieves the least recently accessed key in $O(1)$.
