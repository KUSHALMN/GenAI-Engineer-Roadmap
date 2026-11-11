# 🎯 Technical Interview Questions — Day 05: RAG Metrics & Prefix Sums

### 1. Define Context Precision vs. Context Recall in RAG evaluation.
**Answer:**
- **Context Precision:** The proportion of retrieved chunks that are genuinely relevant to answering the query (signal-to-noise ratio). Higher precision prevents hallucination and token waste.
- **Context Recall:** The proportion of all necessary facts or golden context chunks that were successfully retrieved by the retrieval engine. High recall ensures the LLM has all required evidence.

### 2. Why is prefix sum hashing $O(N)$ for finding subarray sums equaling $K$?
**Answer:**
A subarray sum from index $i$ to $j$ equals `prefixSum[j] - prefixSum[i-1] = K`. By rearranging to `prefixSum[j] - K = prefixSum[i-1]`, we can look up whether the necessary prefix sum occurred previously in $O(1)$ time using a HashMap, reducing an $O(N^2)$ brute-force sweep to a single $O(N)$ pass.
