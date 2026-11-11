# 🎯 Technical Interview Questions — Day 16: PII Masking & 1D Dynamic Programming

## Question 1: How do you implement low-latency, reversible PII redaction for high-throughput LLM pipelines?
**Answer:**
A production PII pipeline operates in two stages:
1. **Pre-LLM Masking:** Inbound text is scanned using high-performance regex or local NER models (e.g. GLiNER, spaCy). PII spans (emails, phone numbers, SSNs, names) are replaced with deterministic surrogate tokens (e.g., `<PII:EMAIL:A9B3>`). The mapping is stored in an encrypted, distributed in-memory cache (Redis) with strict TTLs and tenant isolation.
2. **Post-LLM Re-identification (Demasking):** When the LLM generates a response referencing the surrogate tokens, a deterministic reverse lookup restores the original customer entity before streaming the response back to authorized clients.
3. **Auditability & Zero Retention:** Non-authorized personnel, LLM logs, and training traces only ever record surrogate tokens, guaranteeing GDPR right-to-be-forgotten and HIPAA compliance.

---

## Question 2: In Dynamic Programming, how do you recognize overlapping subproblems and optimize memory from O(N) to O(1)?
**Answer:**
- **State Recurrence:** In problems like House Robber ($DP[i] = \max(DP[i-1], DP[i-2] + nums[i])$) or Fibonacci/Climbing Stairs ($DP[i] = DP[i-1] + DP[i-2]$), the current decision depends strictly on a finite window of previous states (here, just $DP[i-1]$ and $DP[i-2]$).
- **Space Optimization:** Instead of allocating an array `int[] dp = new int[n]`, maintain two variables (`prev1`, `prev2`) updated iteratively. This reduces memory footprint from $O(N)$ to $O(1)$ auxiliary space while retaining $O(N)$ linear time complexity.
