# Day 09: Technical Interview Preparation — QLoRA & LRU Cache

### Q1: What are the three core innovations of QLoRA compared to standard LoRA?
**Answer:**
1. **NF4 (NormalFloat 4-bit):** An information-theoretically optimal quantile quantization data type for normally distributed neural network weights.
2. **Double Quantization (DQ):** Quantizing the quantization constants themselves, saving ~0.37 bits per parameter.
3. **Paged Optimizers:** Using CUDA unified memory to page optimizer states between GPU VRAM and CPU RAM during gradient checkpoints to prevent out-of-memory crashes.

### Q2: Why is Doubly Linked List necessary in LRU cache instead of a Singly Linked List?
**Answer:**
To remove an arbitrary node in $O(1)$ time, we need immediate access to its predecessor node (`node.prev.next = node.next`). In a singly linked list, finding the predecessor requires an $O(n)$ traversal from the head.
