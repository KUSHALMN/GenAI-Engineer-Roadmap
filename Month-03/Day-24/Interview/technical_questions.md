# Interview Questions: Query Routing & Segment Trees

### Q1: How do you implement query routing without introducing high LLM latency?
**Answer**:
1. **Rule-Based Heuristic Filters**: Fast regex checks for greetings, error codes, and SQL keywords take $< 1$ millisecond.
2. **Small Embedding Classifier (SetFit / Logistic Regression on Embeddings)**: Running an SVM or lightweight classifier over the query embedding takes $\sim 2$–$5$ ms.
3. **Small Language Model (SLM)**: Use quantized 0.5B/1B models (e.g. Qwen 2.5 0.5B) for structured JSON classification if complex contextual reasoning is required.

### Q2: Why does a Segment Tree allocate $4 \times N$ array size?
**Answer**:
A Segment Tree is a full binary tree where each leaf corresponds to an element of array $N$.
If $N$ is a power of 2, the number of leaves is $N$ and internal nodes is $N - 1$, totaling $2N - 1$.
If $N$ is not a power of 2, the tree height is $\lceil \log_2 N \rceil$. In the worst case where $N = 2^k + 1$, the next power of 2 is $2^{k+1} \approx 2N$, and the total number of nodes in the full binary tree is $2 \times 2N - 1 \approx 4N$.

### Q3: What is Lazy Propagation in Segment Trees?
**Answer**:
When updating a whole range $[L, R]$ (instead of a single point), a standard segment tree takes $\mathcal{O}(N)$ because it visits all leaves in the range.
**Lazy Propagation** solves this by postponing updates:
- When a node's interval $[start, end]$ lies completely inside $[L, R]$, the node is updated and its children are marked with a "lazy tag" (pending update).
- The children are only updated when a future query or update actually visits them.
- This restores range update time to strictly $\mathcal{O}(\log N)$.
