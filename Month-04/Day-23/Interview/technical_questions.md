# Day 23: Technical Interview Preparation — Multi-Agent Systems & Cycle Detection

### Q1: When is a multi-agent system worth the token overhead compared to a single monolithic agent?
**Answer:**
Multi-agent topologies are justified when:
1. **Specialized Prompts & System Instructions:** A specialized Python code execution agent requires drastically different safety prompts and tool sets than a customer-facing writing agent.
2. **Context Window Partitioning:** Isolating raw tool outputs inside worker subagents prevents the supervisor context window from filling up with noisy logs.
3. **Parallel Task Execution:** Independent sub-investigations can execute concurrently across distinct workers.

### Q2: How does DSU detect cycles in an undirected graph?
**Answer:**
Initially, each vertex is in its own disjoint set. As we process each edge $(u, v)$, we check if `find(u) == find(v)`. If true, both vertices are already connected by a path; adding this edge introduces a cycle. If false, we merge their components using `union(u, v)`.
