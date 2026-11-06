# Day 08: Technical Interview Preparation — Checkpoints and Bitmasks

### Q1: How do idempotency keys prevent duplicate side effects when resuming an agent from a checkpoint?
**Answer:**
When an agent invokes an external side-effecting API (e.g. charging a credit card or provisioning a server), it attaches a deterministic idempotency key (e.g. `hash(session_id, step_index)`). If the agent crashes after the API call but before saving the checkpoint, resuming the agent will re-submit the same idempotency key, allowing the payment gateway to return the previous successful result instead of double-charging.

### Q2: What are the advantages of bitmask enumeration over recursive backtracking for subsets?
**Answer:**
- **Zero Recursion Overhead:** No stack frames allocated; runs in a tight iterative loop.
- **Easy Parallelization:** Any subset index `mask` can be computed independently, making bitmask enumeration trivially parallelizable across threads or GPU cores.
