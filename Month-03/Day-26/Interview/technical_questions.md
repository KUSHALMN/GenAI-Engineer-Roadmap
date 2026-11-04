# Interview Questions: Evaluation Datasets & Bit Manipulation

### Q1: Why must a golden retrieval evaluation set contain "unanswerable" questions?
**Answer**:
A major failure mode of production RAG is **hallucination under absence of evidence**.
If an evaluation dataset only contains answerable questions, a retrieval pipeline that aggressively returns low-confidence irrelevant chunks will score high recall.
Unanswerable questions test whether the pipeline correctly identifies low similarity scores and **abstains** ("I do not have enough evidence to answer this question") rather than hallucinating an answer from irrelevant noise.

### Q2: How does `diff = xor & (-xor)` isolate the rightmost set bit in LeetCode 260?
**Answer**:
`-xor` is computed in two's complement by inverting all bits of `xor` and adding `1`.
All bits to the right of the lowest set bit were $0$ in `xor`, so they become $1$ in `~xor` and flip back to $0$ with $+1$ carry.
The lowest set bit itself was $1$, became $0$ in `~xor`, and turns into $1$ with $+1$.
All bits to the left are inverted.
Thus, bitwise AND `xor & (-xor)` clears all bits except the single lowest set bit.

### Q3: How do you partition an array into two subsets based on `diff`?
**Answer**:
Because `diff` is a bit where the two unique numbers $A$ and $B$ differ (one has bit 0, one has bit 1), checking `(x & diff) == 0` divides the array into two disjoint groups.
- Group 0 contains $A$ plus duplicate pairs.
- Group 1 contains $B$ plus duplicate pairs.
XORing each group independently cancels out all duplicates, isolating $A$ and $B$ in $\mathcal{O}(N)$ time and $\mathcal{O}(1)$ space.
