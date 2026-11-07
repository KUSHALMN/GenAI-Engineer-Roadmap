# Day 26: Technical Interview Preparation — Prompt Versioning & ThreadPool Rejection

### Q1: Why is Prompt Version Control as critical as code version control in GenAI production?
**Answer:**
A prompt is executable code: modifying a single word can alter model output format, cause downstream parsing exceptions, or bypass safety guardrails. Tying application deployments to immutable prompt version hashes ensures telemetry and regressions can be isolated to code vs prompt vs model weight shifts.

### Q2: Compare the four standard Java `RejectedExecutionHandler` policies.
**Answer:**
1. **`AbortPolicy` (Default):** Throws `RejectedExecutionException`.
2. **`CallerRunsPolicy`:** Runs the task directly on the caller thread, naturally throttling submission speed (backpressure).
3. **`DiscardPolicy`:** Silently drops the task without notification.
4. **`DiscardOldestPolicy`:** Evicts the oldest unhandled task in the queue and retries execution.
