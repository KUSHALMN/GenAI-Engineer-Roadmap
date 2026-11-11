# 🎯 Technical Interview Questions — Day 30: Capstone Architecture & Hard Mastery Index

## Question 1: How do you present the architecture of an enterprise LLMOps Evaluation & Governance Platform to staff engineers?
**Answer:**
1. **Pillars of the Architecture:**
   - **Ingress / Gateway Layer:** Edge proxies implementing rate limits, geofenced residency enclaves, and low-latency PII surrogate tokenization.
   - **Quality & Evaluation Core:** Asynchronous evaluation pipelines utilizing multi-modal LLM-as-a-judge calibrators, semantic entropy uncertainty gates, and golden regression datasets.
   - **Governance & Audit Layer:** Immutable model system cards, automated dataset lineage tracking, and EU AI Act / NIST RMF compliance verification.
   - **Observability & FinOps:** Real-time token cost attribution, queueing theory cluster sizing, and circuit-breaker tripping.
2. **Measurable Outcomes:** $0\%$ PII leakage rate, $99.8\%$ safety refusal accuracy, and automated PR quality gate prevention of regression breaches.

---

## Question 2: In LeetCode 41 (First Missing Positive), explain how cyclic sort achieves O(N) time with O(1) space.
**Answer:**
- The first missing positive integer for an array of size $N$ must fall in the range $[1, N + 1]$.
- We place each positive integer $x \in [1, N]$ into its target bucket index $x - 1$ via cyclic swaps (`nums[nums[i]-1] = nums[i]`).
- Each swap places at least one number in its permanent, correct position. Since there are $N$ numbers, at most $N$ swaps can occur across the entire traversal ($O(N)$ total).
- A second linear pass scans indices: the first index where `nums[i] != i + 1` reveals the answer $i + 1$. If all indices match, the answer is $N + 1$.
