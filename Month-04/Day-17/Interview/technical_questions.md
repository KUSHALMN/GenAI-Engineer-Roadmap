# Day 17: Technical Interview Preparation — MCP Resources & Matrix Chain Multiplication

### Q1: What is the semantic difference between MCP Resources and MCP Tools?
**Answer:**
- **Resources (`resources/read`):** Read-only, idempotent data points accessed via standard URIs. Fetching a resource has zero side effects and requires lower security authorization.
- **Tools (`tools/call`):** Executable operations with side effects, compute burdens, or non-deterministic outputs. Require higher authorization and audit logging.

### Q2: Why is Matrix Chain Multiplication an $O(n^3)$ algorithm?
**Answer:**
There are $O(n^2)$ subproblems corresponding to all continuous subchains $(i, j)$ where $1 \le i \le j \le n$. For each subchain of length $L$, the algorithm tests all possible split points $k$ between $i$ and $j-1$ ($O(n)$ choices per state). Thus, overall complexity is $O(n^3)$.
