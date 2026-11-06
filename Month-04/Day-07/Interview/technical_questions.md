# Day 07: Technical Interview Preparation — Workflow Graphs

### Q1: Why do modern agent frameworks (e.g. LangGraph) model agent orchestration as cyclic graphs instead of linear chains?
**Answer:**
1. **Cyclic Revision Loops:** Real tasks require iterative refinement (Draft -> Critique -> Refine -> Critique). Linear chains cannot loop without complex wrapper scripts.
2. **Conditional Branching:** Graphs support dynamic routers that inspect state and branch to specialized agents (e.g., Code Reviewer vs Financial Auditor).
3. **Interruptibility:** Graph edges provide natural pause points where human approval or tool waits can be checkpointed and resumed asynchronously.

### Q2: Why is building a Trie for multiple word search exponentially faster than running standard single-word DFS for each word?
**Answer:**
Running single-word search $K$ times takes $O(K \cdot m \cdot n \cdot 3^L)$. By indexing all words into a Trie, a single simultaneous grid traversal matches common prefixes across all words at once. If cell `'o'` has no children in the Trie, the entire search subtree is pruned in $O(1)$.
