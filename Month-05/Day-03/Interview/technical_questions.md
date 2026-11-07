# Day 03: Technical Interview Preparation — Dataset Cleaning & Red-Black Trees

### Q1: Why is exact deduplication and near-deduplication (MinHash LSH) critical before fine-tuning?
**Answer:**
Duplicate samples in fine-tuning datasets cause models to overfit and memorize specific tokens, increasing loss spikes on general benchmarks and causing repetitive generated patterns (degeneration). Deduplication balances gradient updates across task categories.

### Q2: Compare `HashMap` vs `TreeMap` in Java in terms of time complexity and internal structure.
**Answer:**
- **HashMap:** Array of buckets with LinkedList/Red-Black Tree collision chains. $O(1)$ average time for `get`/`put`. Elements are unordered.
- **TreeMap:** Implements `NavigableMap` using a self-balancing Red-Black Tree. Strict $O(\log n)$ worst-case time for `get`/`put`. Maintains keys in natural or comparator-defined sorted order, enabling range queries like `ceilingKey()` and `subMap()`.
