# Day 19 — DSA & Coding Interview Questions: Heaps & Top-K Problems

In-depth technical breakdown of Heap / PriorityQueue and Selection algorithms frequently asked in FAANG/Tier-1 coding rounds.

---

### Q1: Why use a Min-Heap of size K to find the Kth *Largest* element instead of a Max-Heap?
**Answer:**
- **Min-Heap of size K:**
  - The heap maintains only the $K$ largest elements seen so far.
  - The top element of the Min-Heap is always the **smallest** among those $K$ elements (which is precisely the $K$-th largest overall).
  - Time Complexity: $O(N \log K)$
  - Space Complexity: $O(K)$
- **Max-Heap of all $N$ elements:**
  - Building the heap takes $O(N)$ and extracting $K$ times takes $O(K \log N)$.
  - Time Complexity: $O(N + K \log N)$
  - Space Complexity: $O(N)$
- **Comparison:** When $K \ll N$ (e.g., finding Top 10 elements in 1,000,000 items), the Min-Heap uses drastically less memory ($O(K)$ vs $O(N)$) and runs in stream-friendly constant space.

---

### Q2: Compare Min-Heap vs QuickSelect for Top-K Problems.
**Answer:**

| Metric | Min-Heap / PriorityQueue | QuickSelect (Hoare's Selection) |
| :--- | :--- | :--- |
| **Time Complexity (Avg)** | $O(N \log K)$ | $O(N)$ |
| **Time Complexity (Worst)**| $O(N \log K)$ | $O(N^2)$ (mitigated with random pivot) |
| **Space Complexity** | $O(K)$ | $O(1)$ iterative / $O(\log N)$ recursive |
| **Streaming Data / Online** | ✅ Yes (can process infinite stream) | ❌ No (requires full in-memory array) |
| **Modifies Input Array** | ❌ No | ✅ Yes (in-place partitioning) |

---

### Q3: How do you implement a Max-Heap in Java using `PriorityQueue`?
**Answer:**
Java's `PriorityQueue` is by default a **Min-Heap**. To make it a **Max-Heap**:
1. **Collections.reverseOrder():**
   ```java
   PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
   ```
2. **Lambda Comparator:**
   ```java
   PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b, a));
   ```
3. **Custom Object Comparator:**
   ```java
   PriorityQueue<int[]> maxHeap = new PriorityQueue<>((p1, p2) -> 
       Integer.compare((p2[0]*p2[0] + p2[1]*p2[1]), (p1[0]*p1[0] + p1[1]*p1[1]))
   );
   ```
> ⚠️ **Common Bug**: Avoid `(a, b) -> b - a` when numbers can be negative or large, as integer overflow can cause incorrect sorting. Always use `Integer.compare(b, a)`.

---

### Q4: When is Bucket Sort superior to Heap for Top K Frequent Elements?
**Answer:**
- In **Top K Frequent Elements**, the maximum possible frequency of any element is bounded by the array length $N$.
- By using an array of lists `List<Integer>[] buckets = new List[N + 1]`, we can bucket each element by its frequency count.
- Populating buckets takes $O(N)$, and traversing backwards from frequency $N$ to $1$ takes $O(N)$.
- Total Time: **$O(N)$ strictly linear**, beating the $O(N \log K)$ heap approach when $K$ is large.
