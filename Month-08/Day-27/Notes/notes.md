# 📝 Notes — Day 27: Eval Platform APIs & Monotonic Stack

- **CI/CD Quality Gates:** Block pull request merges if evaluation regression delta $\Delta_{\text{quality}} < -1.5\%$.
- **Histogram Sentinel Bar:** Appending a virtual bar of height 0 at index $n$ automatically flushes all remaining elements from the monotonic stack.
