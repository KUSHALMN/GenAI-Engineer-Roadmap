# Day 31: Technical Interview Preparation — Capstone Benchmark & LRU Cache

### Q1: Summarize the architectural milestones of Month 04 (Agents, MCP & Tool-Use Engineering).
**Answer:**
1. **Tool Engineering:** Moving from raw text generation to typed JSON Schema tool contracts with validation and side-effect declarations.
2. **Agent Loops & State:** From basic ReAct loops to cyclic workflow graphs with immutable state reducers and persistent checkpoints.
3. **Safety & Governance:** Integrating human-in-the-loop approval gates, budget policy circuit breakers, and sandboxed execution environments.
4. **Standardization with MCP:** Implementing Model Context Protocol JSON-RPC 2.0 servers, resources, prompts, and clients.
5. **Multi-Agent Coordination:** Orchestrator-worker patterns, delegation contracts, and result synthesis.

### Q2: Why is Doubly Linked List paired with HashMap the optimal design for LRU Cache?
**Answer:**
HashMap provides $O(1)$ key-to-node lookup. A Doubly Linked List allows $O(1)$ node removal and head insertion without shifting array elements, achieving strict $O(1)$ worst-case time for both `get` and `put`.
