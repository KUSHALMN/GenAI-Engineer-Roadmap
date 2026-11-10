# 🎯 Technical Interview Questions — Day 19: SLOs & Task Scheduler LLD

### 1. Explain the difference between an SLI, an SLO, an SLA, and Error Budget.
**Answer:**
- **SLI (Service Level Indicator):** A quantifiable metric of performance (e.g., % of successful requests with latency < 500ms).
- **SLO (Service Level Objective):** An internal target set by engineering (e.g., 99.9% of requests meet SLI over 30 rolling days).
- **SLA (Service Level Agreement):** A legal contract with financial penalties if SLO is violated.
- **Error Budget:** `1.0 - SLO`. For a 99.9% SLO, the error budget is 0.1%. When the budget is depleted, feature deployments freeze in favor of reliability fixes.

### 2. How do you prevent thread starvation in a multi-tenant Task Scheduler?
**Answer:**
Use fair multi-tenant round-robin or separate tenant priority queues. Rather than a single global queue where one noisy tenant can flood millions of tasks, assign each tenant a virtual concurrency lane or rate-controlled token bucket.
