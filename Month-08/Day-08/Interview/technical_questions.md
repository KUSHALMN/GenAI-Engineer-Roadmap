# 🎯 Technical Interview Questions — Day 08: A/B Testing & Monotonic Stacks

### 1. What guardrail metrics must accompany primary conversion metrics in an LLM A/B experiment?
**Answer:**
Primary metrics (e.g., query completion rate or user thumbs-up) can be artificially inflated by overly verbose or hallucinated pleasantries. Guardrails must include:
- **P95 / P99 Latency:** Ensure new model/prompt does not degrade interactive speed.
- **Token Cost per Query:** Monitor GPU capacity or vendor API bill growth.
- **Refusal / Abstention Rate:** Ensure the new variant is not overly permissive or overly timid.

### 2. How does a monotonic stack achieve $O(N)$ complexity for LC 739 Daily Temperatures?
**Answer:**
Every array index is pushed onto the stack exactly once and popped at most once when a warmer future temperature is encountered. Since each element experiences $O(1)$ operations, the total runtime is strictly $O(N)$, far outperforming the $O(N^2)$ brute force comparison.
