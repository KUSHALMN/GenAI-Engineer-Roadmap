# 🎯 Technical Interview Questions — Day 17: System Cards & 2D Dynamic Programming

## Question 1: What core sections constitute an EU AI Act & NIST compliant AI Model System Card?
**Answer:**
A production Model System Card requires five non-negotiable pillars:
1. **Model Identification & Metadata:** Version, architecture, release date, and maintainers.
2. **Intended Use & Out-of-Scope Declarations:** Explicitly documented functional domains, approved user personas, and prohibited hazardous use-cases.
3. **Training Data & Provenance:** Data sources, licensing audits, synthetic vs human proportions, and PII filtering methods.
4. **Quantitative Benchmark Results:** Standardized accuracy, faithfulness, toxicity, and hallucination scores across golden test suites.
5. **Risk Assessment & Mitigations:** Documented residual risks, safety guardrail specifications, human-in-the-loop fallback procedures, and incident response playbooks.

---

## Question 2: In LeetCode 1143 (LCS), how does space optimization reduce the DP table from O(M*N) to O(min(M,N))?
**Answer:**
- Standard DP maintains a full table `dp[m+1][n+1]` where `dp[i][j]` depends only on `dp[i-1][j-1]`, `dp[i-1][j]`, and `dp[i][j-1]`.
- Because calculating row $i$ only requires entries from row $i-1$ and row $i$, we only need two rows, or a single row of size $\min(M, N) + 1$ with a scalar `prevDiag` holding the old diagonal value `dp[i-1][j-1]`.
- Swapping the shorter string to the inner loop guarantees $O(\min(M, N))$ space, drastically improving L1/L2 CPU cache locality.
