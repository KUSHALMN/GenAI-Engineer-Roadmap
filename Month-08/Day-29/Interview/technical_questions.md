# 🎯 Technical Interview Questions — Day 29: Integrated Governance & Top FAANG Mock

## Question 1: How do you sequence guardrails in an enterprise LLM gateway to minimize latency overhead?
**Answer:**
Guardrails should be sequenced strictly by increasing latency cost:
1. **Stage 1 (< 1ms):** Regex, exact token matchers, PII surrogate masking, IP geofencing, and cached semantic hash hits.
2. **Stage 2 (5–15ms):** Local quantized linear classifier / lightweight BERT models for toxicity, intent classification, and prompt injection detection.
3. **Stage 3 (Async Streaming):** As the primary LLM streams tokens, an asynchronous buffer audits citations and hallucination probability in sliding windows.
4. **Early Exit:** Any violation at an earlier stage terminates the pipeline immediately, protecting downstream GPU budgets.

---

## Question 2: In LeetCode 4 (Median of Two Sorted Arrays), explain why the binary search partition yields O(log(min(M, N))).
**Answer:**
- We partition both arrays such that the combined left halves contain $(M + N + 1) / 2$ elements.
- By running binary search strictly on the smaller array (size $M$), any choice of partition $P_X$ uniquely determines $P_Y = (M + N + 1) / 2 - P_X$.
- The condition for a valid median partition is $maxLeftX \le minRightY$ and $maxLeftY \le minRightX$.
- Since we binary search over the range $[0, M]$, the time complexity is strictly $O(\log(\min(M, N)))$ with $O(1)$ space.
