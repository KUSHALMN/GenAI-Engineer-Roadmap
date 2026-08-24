# Day 21 Resources: StateGraph Agent Architectures & Graph Algorithms

A curated collection of documentation, seminal research papers, tools, and DSA practice references for Day 21.

---

## 🤖 AI & StateGraph Architectures

### Official Documentation & Frameworks
- **[LangGraph Official Documentation](https://langchain-ai.github.io/langgraph/)**: Comprehensive guide to StateGraph concepts, cyclic topologies, conditional edges, and persistence checkpoints.
- **[LangChain Multi-Agent Workflows](https://python.langchain.com/docs/concepts/multi_agent/)**: Collaboration patterns (Supervisor, Hierarchical, Peer-to-Peer).
- **[Groq Cloud Platform Documentation](https://console.groq.com/docs)**: Ultra-low latency LPU inference documentation for sub-second agent reasoning loops.

### Foundational Research Papers
- **[ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)](https://arxiv.org/abs/2210.03629)**: The foundational paper introducing dynamic interleaving of reasoning traces with tool actions.
- **[DeepSeek-V3 Technical Report (DeepSeek AI, 2024)](https://arxiv.org/abs/2412.19437)**: 671B MoE architecture with Multi-Head Latent Attention (MLA) and fine-grained routed experts.
- **[From Local to Global: A Graph RAG Approach (Edge et al., 2024)](https://arxiv.org/abs/2404.16130)**: Combining Knowledge Graphs with Leiden community clustering for global summarization.
- **[Training Compute-Optimal Large Language Models (Hoffmann et al., 2022)](https://arxiv.org/abs/2203.15556)**: Chinchilla scaling laws ($N \sim C^{0.5}, D \sim C^{0.5}$, FLOPs $= 6ND$).
- **[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (Dao et al., 2022)](https://arxiv.org/abs/2205.14135)**: SRAM tiling and exact attention speedups.

---

## 🧩 Data Structures & Algorithms (Graph Mastery)

### LeetCode Problem References
- **[LeetCode 200: Number of Islands](https://leetcode.com/problems/number-of-islands/)** (Medium):
  - Focus: 2D Grid DFS Sink, BFS Queue, Disjoint Set Union (Union-Find).
- **[LeetCode 207: Course Schedule](https://leetcode.com/problems/course-schedule/)** (Medium):
  - Focus: Kahn's Algorithm (BFS In-Degree Topological Sort) and 3-State DFS Cycle Detection.
- **[LeetCode 133: Clone Graph](https://leetcode.com/problems/clone-graph/)** (Medium):
  - Focus: Deep copy of cyclic graphs with `HashMap<Node, Node>` reference isolation.

### Classical Computer Science Literature
- **Tarjan, R. E. (1975)**: *Efficiency of a Good But Not Linear Set Union Algorithm* (Journal of the ACM) - Proof of $O(M \cdot \alpha(N))$ inverse Ackermann bound for Disjoint Set Union.
- **Kahn, A. B. (1962)**: *Topological sorting of large networks* (Communications of the ACM) - The foundational in-degree queue algorithm.
- **Cormen, Leiserson, Rivest, Stein (CLRS)**: *Introduction to Algorithms* - Chapters on Elementary Graph Algorithms, Topological Sort, and Disjoint Sets.
