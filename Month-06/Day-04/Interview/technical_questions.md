# Technical Interview Preparation — Document Layout & Linear Sorting

## 1. Document AI: Resolving Multi-Column Reading Order
**Question:** Why do naive PDF text extractors scramble multi-column academic papers, and how does the Recursive XY-Cut algorithm resolve natural reading order?

**Answer:**
- **Why Naive Extractors Fail:**
  - PDF files store text as raw vector drawing commands (e.g., `BT /F1 12 Tf 72 712 Td (Text) Tj ET`).
  - These commands are indexed by object creation order or typesetting sequence, NOT visual layout order.
  - A naive vertical projection ($y$-coordinate sort) interleaves lines from Column 1 and Column 2: Line 1 (Col 1), Line 1 (Col 2), Line 2 (Col 1)... ruining coherence for LLMs.
- **Recursive XY-Cut Solution:**
  1. Project all bounding boxes onto horizontal ($X$) and vertical ($Y$) projection profiles.
  2. Detect whitespace "gutters" (regions where projection value is zero).
  3. Divide the document canvas recursively:
     - If a horizontal split is found across the whole width (e.g. below a full-width title), slice horizontally.
     - Within column blocks, detect vertical whitespace gutters and slice vertically into distinct columns.
  4. Perform depth-first traversal of the resulting spatial tree: Column 1 blocks are fully ingested before Column 2 blocks.

---

## 2. Linear-Time Sorting Constraints: Counting Sort vs. Radix Sort
**Question:** What are the mathematical constraints and trade-offs of Counting Sort and Radix Sort compared to $O(N \log N)$ comparison-based sorts?

**Answer:**
- **Comparison Lower Bound:**
  - Any decision-tree-based sorting algorithm requires at least $\log_2(N!) \approx N \log_2 N - N \log_2 e = \Omega(N \log N)$ comparisons in the worst case.
- **Counting Sort:**
  - Time: $O(N + K)$, Space: $O(N + K)$ where $K = \max(arr) - \min(arr) + 1$.
  - Constraint: Extremely efficient when $K = O(N)$. Catastrophic when $K \gg N$ (e.g., sorting 10 integers where one is $10^9$ allocates a 1-billion element array).
- **Radix Sort (LSD):**
  - Time: $O(d \cdot (N + B))$ where $d$ is number of digits and $B$ is the base (typically 10 or 256).
  - Advantage: Eliminates large $K$ memory allocation by sorting sub-keys stably.
