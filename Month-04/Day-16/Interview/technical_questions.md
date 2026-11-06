# Day 16: Technical Interview Preparation — MCP Servers & Interval DP

### Q1: How does an MCP Server handle concurrent client requests over stdio vs SSE?
**Answer:**
- **Stdio:** Inherently simplex/duplex point-to-point stream between parent process and child process. Concurrent requests are queued and multiplexed by JSON-RPC `id` correlation.
- **Server-Sent Events (SSE) / HTTP:** Multi-client capable. Clients establish an SSE channel for incoming server events and send POST requests for tool calls, allowing horizontal scaling across container instances.

### Q2: Why is the transition in Burst Balloons formulated around the LAST balloon burst rather than the first?
**Answer:**
If we choose the *first* balloon to burst, the remaining balloons on the left and right become adjacent, creating complex inter-dependencies between subproblems. By choosing the *last* balloon $k$ to burst, $k$ acts as a fixed boundary separating the left $(i, k)$ and right $(k, j)$ subproblems cleanly without boundary leakage.
