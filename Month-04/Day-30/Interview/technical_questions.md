# Day 30: Technical Interview Preparation — Project 4 Production Release

### Q1: What are the core pillars of an enterprise-grade AI Agent readiness review?
**Answer:**
1. **Safety & Permission Boundaries:** High-risk mutating tools require cryptographic tokens or human authorization gates.
2. **Bounded Autonomy:** Hard ceilings for steps, tokens, and wall-clock execution time with loop detection.
3. **Observability & Auditing:** Full OpenTelemetry tracing with correlation IDs recording prompt, tool input/output, and latency.
4. **Resilience & Recovery:** Graceful degradation, self-reflection on tool failure, and zero duplicate side-effects.

### Q2: How does Target Sum reduce to the 0/1 Subset Sum problem?
**Answer:**
Let $P$ be the subset with positive signs and $N$ be the subset with negative signs.
We have: $\sum(P) - \sum(N) = target$ and $\sum(P) + \sum(N) = total$.
Adding both equations: $2\sum(P) = target + total \implies \sum(P) = (target + total) / 2$.
The problem is mathematically equivalent to finding the number of subsets with sum equal to $\sum(P)$.
