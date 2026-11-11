# 🎯 Technical Interview Questions — Day 18: Content Safety & Advanced DP

## Question 1: How do you design a deterministic, multi-tiered content moderation engine for LLMs?
**Answer:**
A production-grade moderation system uses three tiers to balance latency and recall:
1. **Tier 1 (Sub-millisecond Pre-filter):** Deterministic trie-based keyword blocklists and regex matching for high-confidence toxic patterns, zero-tolerance terms, and PII.
2. **Tier 2 (Low-latency Vector Classifier):** Embeddings compared against toxic semantic centroid clusters or a quantized BERT model (e.g. Llama-Guard or Moderation Endpoint), running in 15–30ms.
3. **Tier 3 (LLM Evaluator / Human Escrow):** Ambiguous content falling between the confidence bounds ($0.4 < p < 0.8$) is sent to an asynchronous supervisor model or queued for human review.

---

## Question 2: Explain why Patience Sorting solves Longest Increasing Subsequence in O(N log N) instead of O(N^2).
**Answer:**
- Standard DP checks all previous indices $j < i$ for $nums[j] < nums[i]$, yielding $O(N^2)$ time.
- **Patience Sorting:** We maintain an array `tails` where `tails[k]` stores the smallest tail of all increasing subsequences of length $k+1$.
- `tails` is strictly monotonic (increasing), allowing binary search (`Arrays.binarySearch` or custom lower bound) to locate the position of element $x$ in $O(\log N)$ time.
- For $N$ elements, overall complexity is $O(N \log N)$ time with $O(N)$ space.
