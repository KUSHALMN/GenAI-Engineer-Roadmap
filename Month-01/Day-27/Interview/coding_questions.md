# 💻 Day 27 Coding Interview Questions: Median of Two Sorted Arrays

### Problem: Median of Two Sorted Arrays (LeetCode 4 - Hard / Top FAANG)
**Key Insight (Binary Search on Partition)**:
To find the median of two sorted arrays $A$ and $B$ in $O(\log(\min(m, n)))$:
1. Always binary search on the shorter array (assume $m \le n$).
2. Partition $A$ at index $i$ and $B$ at index $j = \lfloor \frac{m + n + 1}{2} \rfloor - i$.
3. A valid partition satisfies:
   $$\maxLeftA \le \minRightB \quad \text{and} \quad \maxLeftB \le \minRightA$$
4. If $\maxLeftA > \minRightB$, $i$ is too far right $\to$ move binary search left ($high = i - 1$).
5. If $\maxLeftB > \minRightA$, $i$ is too far left $\to$ move binary search right ($low = i + 1$).

**Why $O(\log(\min(m, n)))$?**:
By restricting the binary search domain to $[0, m]$, the search space halves on every step, yielding strictly logarithmic time with $O(1)$ auxiliary memory.
