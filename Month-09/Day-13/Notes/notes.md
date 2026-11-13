# 📝 Notes — Day 13: RingAttention & Parentheses Analysis

- **RingAttention vs TP:** TP parallelizes attention heads across GPUs, capping parallelism at the number of heads (e.g. 32 or 64). RingAttention parallelizes the sequence dimension, scaling independently of head count up to hundreds of GPUs.
- **Stack Base Pointer:** Seeding the stack with index `-1` ensures length calculations `i - stack.peek()` properly include the first character when matching from index 0.
