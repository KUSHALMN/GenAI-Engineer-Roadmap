# 🎯 Technical Interview Questions — Day 22: Pareto Optimization & Bounded Concurrency

## Question 1: How do you construct and navigate the Pareto Frontier for LLM serving architectures?
**Answer:**
1. **Multi-Objective Dimensionality:** The three critical vectors are Quality ($Q$, e.g., MMLU/AlpacaEval), Latency ($L$, TTFT and P95 inter-token latency), and Cost ($C$, GPU instance $/hr / tokens/sec).
2. **Identification of Non-dominated Points:** Point $A$ dominates $B$ if $Q_A \ge Q_B$, $L_A \le L_B$, and $C_A \le C_B$, with at least one strict inequality. The set of points not dominated by any other configuration forms the Pareto frontier.
3. **Dynamic Routing (SLO-driven):** The serving router selects points on the frontier based on inbound SLA: high-tier user queries route to high-quality frontier points, while background bulk jobs route to low-cost frontier points.

---

## Question 2: How do you prevent thread starvation and priority inversion in a Java Semaphore limiter?
**Answer:**
- **Fair vs Unfair Semaphores:** Using `new Semaphore(permits, true)` enforces an internal FIFO queue in the AbstractQueuedSynchronizer (AQS). Threads acquire permits in the order they arrived, preventing thread starvation.
- **Bounded Timeouts:** Calling `tryAcquire(timeout, unit)` rather than blocking indefinitely with `acquire()` ensures worker threads can fail fast and return 429/503 status codes rather than deadlocking thread pool queues.
