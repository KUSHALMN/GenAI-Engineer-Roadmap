# 💻 Day 28 Coding Interview Questions: Word Ladder & Bidirectional BFS

### Problem: Word Ladder (LeetCode 127 - Hard / High-Frequency)
**Key Insight (Bidirectional BFS)**:
In a state graph where branching factor is $b \approx 26 \times M$ and depth is $d$:
- Standard unilateral BFS explores $O(b^d)$ nodes.
- **Bidirectional BFS** explores from both `beginWord` and `endWord` simultaneously, meeting in the middle at depth $d/2$.
- The total nodes visited becomes $O(2 \cdot b^{d/2})$, transforming exponential growth into manageable memory sizes.

**Optimization Trick**:
At each step, always swap pointers to expand whichever frontier set is currently smaller:
```java
if (forwardSet.size() > backwardSet.size()) {
    Set<String> temp = forwardSet;
    forwardSet = backwardSet;
    backwardSet = temp;
}
```
This guarantees minimal fan-out at every level.
