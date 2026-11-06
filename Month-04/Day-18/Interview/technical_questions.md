# Day 18: Technical Interview Preparation — MCP Clients & Tree DP

### Q1: How does an MCP client ensure child server processes do not become zombie processes?
**Answer:**
1. **Standard In/Out Closing:** When the client closes its `stdin` pipe to the child process, standard Unix/Windows processes receive EOF and gracefully exit.
2. **Context Managers & Subprocess Termination:** The client uses Python context managers (`__enter__` / `__exit__`) or JVM shutdown hooks to explicitly call `process.terminate()` and `process.wait(timeout=2)`.
3. **Heartbeat Pings:** Periodic ping/pong health requests ensure frozen processes are killed.

### Q2: Why is post-order traversal optimal for Tree DP?
**Answer:**
In a tree, a parent node cannot know whether it is optimal to be selected until the full subtrees of both its left and right children are resolved. Post-order traversal guarantees that children states are computed bottom-up first before evaluating the parent.
