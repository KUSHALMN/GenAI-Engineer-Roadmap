# 📝 Notes — Day 06: ZeRO Memory Optimization & Wildcard Trie

- **ZeRO-Offload:** When GPU VRAM is exhausted, ZeRO-Offload delegates FP32 Adam optimizer updates to host CPU memory over PCIe, trading compute cycles for near-infinite parameter scale.
- **Trie Depth Bounds:** The recursion stack depth in Trie wildcard DFS is strictly bounded by the word length $M$ ($O(M)$ auxiliary stack space).
