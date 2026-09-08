# 💻 Day 26 Coding Interview Questions: Merge k Sorted Lists

### Problem: Merge k Sorted Lists (LeetCode 23 - Hard / High-Frequency)
**Key Insight (Min-Heap)**:
We can merge $k$ sorted linked lists simultaneously by maintaining a Min-Heap of size $k$ containing the current heads of each active list.
At each step:
1. Extract the minimum node from the Min-Heap ($O(\log k)$).
2. Attach it to our merged result list.
3. If the extracted node has a `.next`, push `.next` into the Min-Heap ($O(\log k)$).

**Total Complexity**:
- $N$ total elements across all $k$ lists.
- Each insertion and deletion in the heap of size $k$ costs $O(\log k)$.
- **Time Complexity**: $O(N \log k)$.
- **Space Complexity**: $O(k)$ for the priority queue.

**Divide-and-Conquer Alternative**:
Pair lists iteratively ($L_0 + L_1, L_2 + L_3 \dots$) and merge in $\lceil \log_2 k \rceil$ levels. Each level touches all $N$ nodes, yielding the same $O(N \log k)$ time with $O(1)$ extra space.
