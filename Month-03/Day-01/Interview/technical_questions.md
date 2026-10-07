# 🎯 Day 01 (Month 03) Technical Interview Questions & Answers

## 1. What is "Lost in the Middle" phenomenon in LLM context windows, and how does Context Engineering solve it?
**Answer:**
Research (Liu et al., 2023) demonstrates that Large Language Models achieve highest retrieval and reasoning accuracy for information placed at the extreme beginning (primacy effect) or extreme end (recency effect) of their input context prompt.
Information located in the middle 60% of an 8k or 128k prompt experiences significant recall degradation ("lost in the middle").
**Mitigations**:
1. **Re-ordering & Prioritization**: Place critical user persona, instructions, and top-1 retrieved documents either at the immediate start of the system prompt or right before the user's latest turn.
2. **Abstractive Summarization**: Compress long conversational chit-chat into concise bullet summaries rather than retaining raw verbatim messages.
3. **Episodic Memory Stores**: Decouple long-term user facts from short-term context windows, retrieving only the 2-3 most semantically relevant facts dynamically.

---

## 2. Compare Sliding Window Memory vs. Summary Memory vs. Vector Episodic Memory.
**Answer:**
- **Sliding Window Memory (Buffer Window)**: Retains the last $K$ turns verbatim. Pros: Simple, zero additional LLM costs. Cons: Forgets critical instructions spoken 10 turns earlier once pushed out of window.
- **Summary Memory**: An LLM periodically compresses past turns into a running text narrative. Pros: Preserves conversational trajectory. Cons: Adds extra LLM latency and token costs on every summarization pass.
- **Vector Episodic Memory**: Stores discrete facts in an embedding database. When the user asks a question, semantic search fetches only relevant facts into context. Pros: Infinite memory capacity across weeks/months. Cons: Retrieval precision depends heavily on embedding quality.

---

## 3. How does Disjoint Set Union (DSU) achieve near $O(1)$ amortized time per operation?
**Answer:**
A naive union-find tree can degenerate into a linked list of depth $N$, yielding $O(N)$ find operations.
DSU employs two optimizations:
1. **Path Compression**: During `find(x)`, every traversed node's parent pointer is updated to point directly to the root (`parent[x] = find(parent[x])`).
2. **Union by Rank / Size**: When merging two disjoint sets, always attach the shallower tree under the root of the deeper tree.
Together, these guarantee an amortized time complexity of $O(\alpha(N))$ per operation, where $\alpha$ is the Inverse Ackermann Function. Because $\alpha(N) \le 4$ for any $N \le 10^{80}$ (atoms in the universe), operations run in effectively constant time $O(1)$.
