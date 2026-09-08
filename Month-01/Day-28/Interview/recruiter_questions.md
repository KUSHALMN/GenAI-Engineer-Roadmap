# 💼 Day 28 Recruiter & System Architecture Interview Questions

### 1. "How do you secure autonomous AI agents with access to tools and databases?"
**Talking Points**:
- "We adhere to the Principle of Least Privilege:
  1. Read-only database credentials for search tools; destructive actions (DROP, DELETE, UPDATE) require explicit human-in-the-loop (HITL) authorization tokens.
  2. Strict parameter validation via Pydantic on tool arguments.
  3. Context segregation: Retrieved external text is sanitized to neutralize indirect prompt injections before passing into the tool-calling agent loop.
  4. Network egress controls: The execution runtime cannot make arbitrary HTTP requests to external domains without allowlist approval."

### 2. "What is your philosophy on AI safety vs. application utility?"
**Talking Points**:
- "Security cannot be an afterthought that bricks application speed or usability.
- We implement tiered defense: fast regex and canary checks run in under 2ms at the ingress proxy.
- For ambiguous or high-risk actions, we escalate to secondary classifier judges or human approval, maintaining high availability for benign queries while closing threat vectors."
