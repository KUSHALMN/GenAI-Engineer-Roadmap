# Day 20: Coding & Algorithms Interview Questions

---

### Q1: In the "Number of Islands" problem (LeetCode 200), why is BFS space complexity $O(\min(M, N))$ while DFS space complexity can degrade to $O(M \times N)$?

#### Answer & Analysis:
- **DFS Stack Depth**:
  - In a worst-case scenario where the entire $M \times N$ grid is land (`'1'`), a recursive DFS path can wind in a serpentine or spiral pattern across every single cell before unwinding.
  - The maximum depth of the call stack is $M \times N$, leading to $O(M \times N)$ auxiliary stack space.
- **BFS Queue Width**:
  - BFS expands outward from the starting cell in concentric wavefronts (Manhattan distance contours).
  - In a 2D matrix, the maximum number of cells on any single wavefront diagonal cannot exceed the minimum of the grid dimensions: $\min(M, N)$.
  - Hence, the queue size is strictly bounded by $O(\min(M, N))$.

---

### Q2: When cloning a graph (LeetCode 133), why must we track visited nodes using a map of `(OriginalNode -> ClonedNode)` rather than just a set of `OriginalNode`?

#### Answer & Analysis:
- In graph cloning, whenever an already-visited neighbor is encountered (due to cycles or shared ancestors), the current clone node must still attach a reference to the **cloned version** of that neighbor.
- A simple `Set<Node>` only tells us *if* a node was visited, but does not provide access to the newly instantiated copy.
- A `Map<Node, Node>` stores the bidirectional bridge:
  ```java
  visited.get(curr).neighbors.add(visited.get(neighbor));
  ```
- This guarantees deep memory isolation and avoids infinite recursion on cyclic edges.

---

### Q3: Explain how Kahn's Algorithm (BFS) and 3-State DFS differ when detecting cycles in a directed graph.

#### Answer & Analysis:
- **Kahn's Algorithm (In-Degree BFS)**:
  - Tracks incoming edges (`inDegree[v]`).
  - Vertices with `inDegree == 0` have no dependencies and are processed first.
  - As nodes are processed, their outgoing edges are removed, reducing neighbors' in-degrees.
  - If a cycle exists, nodes within the cycle never reach an in-degree of 0 and are never enqueued. Thus, `processedCount < numNodes`.
- **3-State DFS Coloring**:
  - Uses 3 states: `0 (Unvisited)`, `1 (Visiting / In Call Stack)`, `2 (Visited)`.
  - If DFS encounters a neighbor marked `1 (Visiting)`, it has detected a **back-edge** to an active ancestor in the recursion stack, proving a directed cycle exists.
- **Complexity**: Both have optimal $O(V + E)$ Time and $O(V + E)$ Space.

---

### Q4: How do you prevent StackOverflowError in Java when performing DFS on extremely large graphs or deep grids?

#### Answer & Analysis:
1. **Iterative DFS with Explicit Stack**:
   - Replace recursive calls with an explicit `Deque<int[]>` on the heap.
   ```java
   Deque<int[]> stack = new ArrayDeque<>();
   stack.push(new int[]{r, c});
   while (!stack.isEmpty()) {
       int[] curr = stack.pop();
       // process neighbors...
   }
   ```
2. **Switch to BFS with Queue**:
   - BFS naturally uses heap memory via `Queue<int[]> queue = new LinkedList<>()`, avoiding thread stack limits.
3. **Disjoint Set Union (DSU / Union-Find)**:
   - For undirected connected components, Union-Find with path compression operates in near $O(1)$ iterative time without deep call stacks.

---

### Q5: What is the Time & Space Complexity of BM25 Inverted Index Search across $N$ documents with average length $L$?

#### Answer & Analysis:
- **Indexing Phase**:
  - Tokenizing and building inverted index: $O(N \times L)$ time and space.
- **Query Phase (with $Q$ query terms and top-$K$ heap)**:
  - Fetching postings lists for $Q$ terms: $\sum_{t=1}^Q \text{DF}(t)$ operations.
  - Scoring and ranking via Min-Heap of size $K$: $O(D_q \log K)$, where $D_q$ is the number of documents matching at least one query term.
  - Total Query Time: $O(D_q \log K) \ll O(N \times L)$, providing sub-millisecond retrieval.
