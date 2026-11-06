# Day 24: Technical Interview Preparation — Agent Delegation & Quickselect

### Q1: How do you resolve conflicting observations returned by two delegated subagents?
**Answer:**
1. **Confidence & Source Attribution:** Subagents attach certainty scores and raw source citations to their findings.
2. **Deterministic Rules Engine:** Apply business logic precedence (e.g. Security Auditor findings take precedence over Feature Developer claims).
3. **Judge Agent / Human Escalation:** If ambiguity persists, route the conflicting outputs to a dedicated Critic/Judge LLM or flag for human review.

### Q2: Why is Quickselect on average $O(n)$ while QuickSort is $O(n \log n)$?
**Answer:**
QuickSort recursively sorts *both* sides of the partitioned array ($T(n) = 2T(n/2) + O(n) \implies O(n \log n)$). Quickselect discards one partition and only recurses into the side containing the target index ($T(n) = T(n/2) + O(n) = n + n/2 + n/4 + \dots \le 2n = O(n)$).
