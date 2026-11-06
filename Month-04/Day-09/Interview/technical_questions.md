# Day 09: Technical Interview Preparation — Human-in-the-Loop & Dynamic Programming

### Q1: What architectural patterns enable asynchronous Human-in-the-Loop (HITL) without blocking the worker process?
**Answer:**
1. **Webhook / Callback Architecture:** When a high-risk tool is triggered, the agent generates an approval ticket, writes state to persistent DB, and enters `AWAITING_INPUT`.
2. **Slack / Email Notification:** A notification service pings the human approver with "Approve" / "Reject" interactive buttons.
3. **Resumption via Event Bus:** When the webhook receives an approval payload, it emits a message to the task queue containing the ticket ID, re-hydrating the agent state to continue execution.

### Q2: How does dynamic programming reduce exponential recursive Fibonacci/House Robber to $O(n)$?
**Answer:**
The naive recursive tree computes overlapping subproblems redundantly ($O(2^n)$). Dynamic programming enforces memoization or bottom-up tabulation so each subproblem state $dp[i]$ is calculated exactly once, collapsing the time complexity to $O(n)$.
