# Day 21: Coding Interview Questions & Answers
## Focus: Graph Algorithms, Traversal Complexity, Deep Copy, and Topological Sort

---

### Q1: Compare DFS vs BFS for 2D Grid Traversal (e.g. *Number of Islands*). When is BFS strictly preferred over DFS in production systems?

**Answer:**
1. **Time Complexity**:
   - Both DFS and BFS visit each cell at most a constant number of times (typically 4 orthogonal checks), achieving $O(M \times N)$ time complexity.
2. **Space Complexity Comparison**:
   - **DFS (Recursion Call Stack)**: Worst-case space is $O(M \times N)$ when the entire grid is land (e.g. a snake or solid land matrix). In languages with default recursion limits (Python: 1000, Java: dependent on thread stack size `Xss`), large matrices ($1000 \times 1000$) will trigger a `StackOverflowError` or `RecursionError`.
   - **BFS (Queue)**: The maximum number of elements in the BFS queue at any given level is proportional to the grid diagonal / perimeter: $O(\min(M, N))$.
3. **Production Preference**:
   - In distributed graph processing, web crawling, or high-throughput microservices, **BFS is preferred** because:
     - It avoids recursion call stack overflow.
     - It guarantees shortest path discovery in unweighted graphs.
     - Memory allocation is bounded and explicitly controllable via heap queues.

---

### Q2: Why is Kahn's Algorithm (BFS In-Degree) preferred over DFS 3-State coloring when generating an actual Topological Sort order?

**Answer:**
1. **Direct Cycle Detection + Order Generation**:
   - Kahn's algorithm maintains an `inDegree` array for all vertices.
   - Vertices with `inDegree == 0` have no dependencies and are processed immediately in natural dependency order (prerequisites first).
   - As each course is completed, outgoing edge counts are decremented, unlocking subsequent courses.
2. **Readability & Predictable Memory**:
   - Kahn's algorithm is completely iterative, avoiding deep recursion trees.
   - If `processedCount < numCourses`, cycle detection is trivial without needing post-order stack reversal.
3. **DFS Alternative**:
   - DFS requires maintaining a post-order traversal stack and reversing it at the end.
   - Cycle detection requires 3-state tracking (`UNVISITED`, `VISITING`, `VISITED`).

---

### Q3: Explain why a naive shallow copy or simple traversal fails when cloning a graph with cycles, and how `HashMap<Node, Node>` guarantees correct deep copy.

**Answer:**
1. **Failure of Naive Copy**:
   - If a graph contains cycles ($A \to B \to C \to A$), traversing without a reference registry results in an **infinite loop**, continuously creating new copies of $A, B, C$ until out of memory.
   - Shallow copying only duplicates node wrappers while keeping pointers referencing original neighbor instances, violating memory isolation.
2. **`HashMap<Node, Node>` Invariant**:
   - The map serves a dual purpose: **Visited Set** and **Pointer Lookup**.
   - Before instantiating or exploring a neighbor, check `if (map.containsKey(neighbor))`.
   - If present, connect `clonedCurrent.neighbors.add(map.get(neighbor))` without recursing.
   - If absent, instantiate `new Node(neighbor.val)`, record in map, and proceed.
   - This ensures exactly $V$ nodes and $E$ edges are instantiated, maintaining $O(V + E)$ time and space complexity.

---

### Q4: What is the Inverse Ackermann Function $\alpha(N)$, and why does Disjoint Set Union (Union-Find) achieve $O(M \cdot \alpha(N))$ nearly-linear time?

**Answer:**
1. **Path Compression**:
   - During `find(x)`, every node along the path is re-parented directly to the root: `parent[i] = find(parent[i])`.
   - Flattens tree depth to $O(1)$ on subsequent queries.
2. **Union by Rank / Size**:
   - Always attach the shorter tree under the root of the taller tree, bounding maximum height to $O(\log N)$.
3. **Combined Complexity**:
   - Tarjan proved that applying both Path Compression and Union by Rank reduces the amortized cost per operation to $O(\alpha(N))$, where $\alpha$ is the inverse Ackermann function.
   - For all conceivable physical inputs ($N \le 10^{80}$, the number of atoms in the observable universe), $\alpha(N) \le 4$. Thus, DSU operations run in effective amortized $O(1)$ time.
