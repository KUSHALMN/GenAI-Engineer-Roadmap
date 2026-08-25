# Month 01 - Day 22 Study Notes: Agent Memory & Checkpointing Systems + Multi-Source Graph Algorithms

---

## 📌 Executive Summary

Day 22 deepens our engineering capabilities in **Persistent Agent State & Memory Architecture** while expanding Graph DSA mastery to **Multi-Source BFS** and **Connected Component Counting**.

Key pillars mastered:
1. **Agent Memory Architecture & State Checkpointing**:
   - Short-term working memory vs Long-term episodic/semantic memory.
   - Graph-level state checkpointing: saving immutable snapshots indexed by `thread_id` and `checkpoint_id`.
   - Multi-turn conversational buffer compaction and cross-turn fact extraction.
   - Time-Travel debugging: rolling back execution to any prior checkpoint state and branching new trajectories.
2. **Graph Algorithms (DSA in Java)**:
   - *Number of Provinces* (LeetCode 547): Graph connected component counting on Adjacency Matrix using DFS, BFS, and DSU.
   - *Rotting Oranges* (LeetCode 994): Multi-Source Breadth-First Search (BFS) level-by-level propagation.
   - *Course Schedule* (LeetCode 207): Kahn's BFS In-Degree Topological Sort & 3-State DFS Coloring.

---

## 🧠 Part 1: Agent Memory & Checkpointing Architecture

### 1. Memory Taxonomy in Autonomous Systems

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT MEMORY TAXONOMY                    │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Working / Ephemeral State  │ 2. Episodic / Session Memory  │
│ - Current graph node state   │ - Multi-turn conversational  │
│ - Intermediate tool outputs  │   buffers & key facts        │
│ - Cleared upon run finish    │ - Compacted context windows  │
├──────────────────────────────┼──────────────────────────────┤
│ 3. Semantic / Long-Term      │ 4. Execution Checkpointer    │
│ - Vector embeddings / BM25   │ - Immutable step snapshots   │
│ - Knowledge bases & papers   │ - Enables time-travel & HITL │
└──────────────────────────────┴──────────────────────────────┘
```

### 2. Checkpointing Mechanics

Every node transition in the StateGraph executes a persist operation:
```python
checkpoint_id = memory_store.save_checkpoint(
    thread_id=thread_id,
    step_index=step_idx,
    node_name=curr_node_name,
    state=state
)
```

**Benefits of Checkpointing:**
1. **Zero-Data-Loss Fault Recovery**: If a worker or pod crashes mid-execution, reload the latest checkpoint record by `thread_id` and continue without re-executing completed tool calls.
2. **Human-in-the-Loop (HITL) Pauses**: High-risk tool calls pause at node entry, persist state, and wait for external approval before progressing.
3. **Time-Travel & Branching**: Replay the agent from step 2 with a modified user instruction or altered state parameter.

---

## 🧩 Part 2: Graph Theory & Multi-Source BFS

### 1. Multi-Source BFS (*Rotting Oranges - LeetCode 994*)
- Unlike single-source BFS which starts at $(0, 0)$ or a single vertex, **Multi-Source BFS** initializes the queue with **ALL initial source vertices simultaneously**.
- All sources expand outward in parallel wave fronts, level by level ($T = 0, T = 1, T = 2, \dots$).
- **Algorithm**:
  1. Iterate over grid: push all `grid[r][c] == 2` into `Queue<int[]>`, count fresh oranges `grid[r][c] == 1`.
  2. While queue is not empty and `freshCount > 0`:
     - Pop all elements in the current queue level (`int levelSize = queue.size()`).
     - For each rotten orange, infect adjacent unrotten neighbors (`grid[nr][nc] = 2`), decrement `freshCount`, and push `(nr, nc)` to queue.
     - Increment `minutes`.
  3. If `freshCount == 0`, return `minutes`, else return `-1`.
- **Complexity**: Time $O(M \times N)$, Space $O(M \times N)$.

---

### 2. Number of Provinces (*LeetCode 547*)
- Given $N \times N$ matrix `isConnected`:
  - DFS / BFS: Maintain `boolean[] visited` of size $N$. Loop $i = 0 \dots N-1$, whenever `!visited[i]`, increment `provinces` and traverse connected cluster.
  - Disjoint Set Union (DSU): Initialize $N$ disjoint sets. For each edge $(i, j)$ where $j > i$, perform `union(i, j)`. Number of provinces equals final `uf.getCount()`.
- **Complexity**: Time $O(N^2 \cdot \alpha(N))$, Space $O(N)$.

---

## 🎯 Summary Checklist
- [x] Implemented `MemoryStore` for step-level checkpointing and time-travel rollbacks.
- [x] Implemented `SessionManager` for multi-turn conversational context compaction.
- [x] Solved LeetCode 547 (*Number of Provinces*) with DFS, BFS, and DSU.
- [x] Solved LeetCode 994 (*Rotting Oranges*) with Multi-Source BFS.
- [x] Solved LeetCode 207 (*Course Schedule*) with Topological Sort.
