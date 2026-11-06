# Day 22: Technical Interview Preparation — Async Tasks & Topological Sort

### Q1: How do you handle long-running tools (e.g. 5-minute database backups) in synchronous LLM agent loops?
**Answer:**
1. **Asynchronous Handshake (`202 Accepted`):** The tool returns immediately with a `task_id` and initial status `QUEUED`.
2. **Notification / Polling Protocol:** The agent can either yield execution and await an MCP progress notification or enter a non-blocking polling state.
3. **Cancellation Token:** The client provides a cancellation token allowing the user to terminate the agent turn without leaving orphan background jobs.

### Q2: How does level-order BFS in Kahn's algorithm compute the minimum semesters in Parallel Courses?
**Answer:**
All courses with `inDegree == 0` at any time have all their prerequisites satisfied and can be taken concurrently in the same semester. Processing the queue level by level increments the semester counter once per batch, finding the length of the longest dependency path in the DAG.
