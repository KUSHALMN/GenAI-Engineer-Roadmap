# Day 20: Technical Interview Preparation — MCP Authorization & Dijkstra

### Q1: How do you enforce Least Privilege access control on an MCP tool catalog?
**Answer:**
1. **Scoped Capabilities:** Issue JWTs containing scoped claims (e.g. `scopes: ["read:reports"]`).
2. **Tool Gateway Interceptor:** Before executing `tools/call`, compare caller token scopes against the tool's required permissions.
3. **Dynamic Filtering:** In `tools/list`, only return tools the caller has permissions to execute, preventing model hallucination of unauthorized actions.

### Q2: Why is Dijkstra's algorithm unsuitable for graphs with negative edge weights?
**Answer:**
Dijkstra greedily marks nodes as "settled" when they are popped from the priority queue under the invariant that edge costs are non-negative. If negative edges exist, a shorter path to a previously settled node might be discovered later, breaking the invariant and requiring algorithms like Bellman-Ford.
