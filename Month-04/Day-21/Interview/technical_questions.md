# Day 21: Technical Interview Preparation — MCP Security & Disjoint Set Union

### Q1: What is the Confused Deputy problem in tool-augmented AI agents?
**Answer:**
A confused deputy vulnerability occurs when an unprivileged user prompts an LLM agent to invoke a privileged tool that the agent possesses permission for, but the user does not. The agent acts as an unwitting deputy, executing unauthorized operations on the user's behalf.
*Mitigation:* Pass caller authorization tokens down to the tool level and enforce role-based access control inside the tool itself.

### Q2: How does Path Compression optimize DSU operations?
**Answer:**
During `find(x)`, path compression sets the parent of every visited node directly to the root of the tree. This flattens the tree structure, ensuring subsequent `find()` operations on those nodes run in amortized near-constant $O(\alpha(N))$ time.
