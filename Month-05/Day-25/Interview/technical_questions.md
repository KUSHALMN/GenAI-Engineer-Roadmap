# Day 25: Technical Interview Preparation — Model Routing & TTL Cache

### Q1: How does model routing optimize the Pareto frontier of cost versus quality?
**Answer:**
Over 70% of enterprise queries (simple extractions, classification, greetings, formatting) do not require costly frontier models (e.g. GPT-4o or Claude 3.5 Sonnet). A classifier router dispatches simple tasks to compact 3B/8B models (saving 80-90% cost and reducing latency) while reserving large models for complex reasoning.

### Q2: How do you prevent memory leaks from expired keys in a TTL Cache if keys are never accessed again?
**Answer:**
Passive eviction (checking on `get()`) fails to free memory for keys that are written once and never queried again. Production systems add an active background eviction thread (e.g. `ScheduledExecutorService`) that periodically samples random keys and purges expired ones, or maintains a `DelayQueue` of expiration events.
