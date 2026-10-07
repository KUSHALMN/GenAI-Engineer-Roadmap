# 🎯 Day 30 Technical Interview Questions & Answers

## 1. What is the Model Context Protocol (MCP), and why is it replacing ad-hoc tool integrations?
**Answer:**
**Model Context Protocol (MCP)**, open-sourced by Anthropic, is an open standard that connects AI assistants to secure enterprise data systems, tools, and developer environments.
- **Before MCP**: Every AI product had bespoke, incompatible plugins and proprietary schemas (OpenAI Actions, LangChain Tools, custom REST APIs). Developers had to write $N \times M$ custom connectors.
- **With MCP**: Tools and context resources are exposed through standardized **JSON-RPC 2.0** transports (stdio or SSE). Any MCP client (Claude Desktop, IDEs, autonomous agents) can discover (`tools/list`, `resources/list`) and invoke tools (`tools/call`) seamlessly without rewriting code.

---

## 2. Compare Dijkstra's Algorithm vs. Bellman-Ford for Shortest Path problems.
**Answer:**
- **Dijkstra’s Algorithm**:
  - *Strategy*: Greedy algorithm utilizing a Min-Heap. Always processes the unvisited node with the smallest known distance.
  - *Time Complexity*: $O((V + E) \log V)$ with adjacency list and binary heap.
  - *Constraint*: Cannot handle negative weight edges.
- **Bellman-Ford Algorithm**:
  - *Strategy*: Dynamic Programming via iterative edge relaxation across $V-1$ iterations.
  - *Time Complexity*: $O(V \cdot E)$.
  - *Advantages*: Handles negative edge weights and can detect negative weight cycles.
  - *Bounded Stops (LC 787)*: When finding shortest path with at most $K$ stops, Bellman-Ford naturally bounds paths by performing exactly $K+1$ iterations.

---

## 3. How does MCP handle security, authorization, and resource sandboxing?
**Answer:**
1. **URI-based Sandboxing**: Resources are addressed via distinct schemes (`file://`, `postgres://`, `system://`) restricting the server's read scope.
2. **Explicit User Consent**: In production MCP architectures, tool calls that modify state (write/delete) prompt human confirmation before execution.
3. **Isolated Transport**: StdIO transport runs the MCP server as an isolated sub-process with restricted OS capabilities.
