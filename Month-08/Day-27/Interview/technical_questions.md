# 🎯 Technical Interview Questions — Day 27: Evaluation API & Monotonic Stack

## Question 1: How do you architect a high-throughput, asynchronous evaluation platform API for enterprise CI/CD?
**Answer:**
1. **Asynchronous Job Ingestion:** The client (GitHub Actions, GitLab CI) submits an evaluation payload to the `/v1/evaluations/run` endpoint, which validates schemas and places a job message onto a Kafka or RabbitMQ queue, returning a `202 Accepted` with a `run_id`.
2. **Worker Pool Execution:** Scalable Celery/Temporal worker clusters pull eval tasks, orchestrating batched parallel LLM calls with rate limiters.
3. **Webhook Callback / Quality Gate:** When complete, worker nodes compute statistical metrics, persist results in PostgreSQL/ClickHouse, and trigger a webhook notification back to GitHub Actions with a pass/fail commit status check.

---

## Question 2: In LeetCode 84 (Largest Rectangle in Histogram), explain why a Monotonic Stack finds the largest rectangle in O(N).
**Answer:**
- A monotonic strictly increasing stack stores indices of bars in non-decreasing order of height.
- When a bar of height $H$ is encountered that is *shorter* than the bar at the top of the stack, the taller bar cannot extend any further to the right.
- Popping the taller bar allows us to compute its maximum possible rectangle area:
  - Height = popped bar's height.
  - Width = distance between the current index $i$ and the new stack top: `i - stack.peek() - 1` (or $i$ if stack is empty).
- Each index is pushed and popped at most once, yielding strictly $O(N)$ linear time.
