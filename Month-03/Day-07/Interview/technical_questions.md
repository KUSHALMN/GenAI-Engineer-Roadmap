# 💬 Day 07: SSE Streaming & Kth Smallest in BST Interview Questions

### Q1: Compare Server-Sent Events (SSE) vs WebSockets for LLM chat completions.
**Answer:**
- **SSE (Server-Sent Events):**
  - Unidirectional (server $\rightarrow$ client) over standard HTTP/1.1 or HTTP/2.
  - Built-in browser reconnection (`EventSource`), message IDs, and comment heartbeats (`: ping`).
  - Seamlessly traverses corporate proxies, firewalls, and load balancers because it uses plain HTTP request/response streaming.
  - Ideal for LLM generation where user sends 1 prompt and LLM streams back $N$ tokens.
- **WebSockets:**
  - Full-duplex bidirectional communication requiring protocol upgrade (`ws://` / `wss://`).
  - Heavier infrastructure footprint, stateful TCP connection mapping across load balancers.
  - Better suited for multiplayer gaming, live video sync, or continuous bi-directional voice streams.

---

### Q2: How does Morris Traversal achieve $\mathcal{O}(1)$ auxiliary space during BST Inorder Traversal?
**Answer:**
Morris Traversal temporarily threads the tree by pointing the rightmost child of the current node's left subtree (the inorder predecessor) back to the current node:
`pred.right = curr`
When the traversal later circles back along this thread, it detects that `pred.right == curr`, restores the tree structure by setting `pred.right = null`, visits `curr`, and moves right. This visits every node in inorder without recursion stack or explicit stack memory.
