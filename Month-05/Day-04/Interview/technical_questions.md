# Day 04: Technical Interview Preparation — Data Leakage & PriorityQueue

### Q1: What is "Data Contamination / Leakage" in LLM fine-tuning and evaluation?
**Answer:**
Data leakage occurs when evaluation prompts or test benchmarks exist in the training corpus (either verbatim or semantically identical). This produces artificially high benchmark scores while concealing the model's inability to generalize to unseen real-world user queries.

### Q2: How does a Min-Heap of size $k$ solve the Top-$K$ problem in $O(n \log k)$ instead of $O(n \log n)$?
**Answer:**
Instead of sorting all $n$ elements in $O(n \log n)$, we push elements into a min-heap. Whenever heap size exceeds $k$, we evict the smallest element in $O(\log k)$. After processing all $n$ elements, the heap retains only the $k$ largest elements.
