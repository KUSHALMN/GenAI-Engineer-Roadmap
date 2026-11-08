# Engineering Notes — Day 07: Vector Embeddings & Sliding Window Mechanics

## 1. Cross-Modal Cosine Metric
$$\text{Cosine}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
When vectors are L2-normalized ($||A||_2 = 1$), cosine similarity simplifies to the dot product $A \cdot B$.

## 2. Sliding Window Invariants
- Window boundaries `[left, right]`.
- Expand `right` until condition is satisfied.
- Contract `left` while condition remains satisfied to find the minimal window.
