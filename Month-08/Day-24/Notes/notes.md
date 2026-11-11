# 📝 Notes — Day 24: Chaos Testing & Hard Algorithms Mock A

- **Exponential Backoff Jitter:** $t = \min(t_{\max}, t_{\text{base}} \times 2^{\text{attempt}}) \times (1 \pm \text{rand}(0, 0.25))$ to eliminate thundering herd synchronization.
- **LC 23 Heap Complexity:** Merging $K$ lists of total size $N$ takes $O(N \log K)$ time and $O(K)$ space for the priority queue.
