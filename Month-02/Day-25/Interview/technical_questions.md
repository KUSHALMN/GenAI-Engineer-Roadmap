# 🎯 Day 25 Technical Interview Questions & Answers

## 1. What is the "Thundering Herd" problem in LLM retries, and how does Full Jitter mitigate it?
**Answer:**
When an upstream LLM API (such as Groq or OpenAI) suffers a brief outage or rate limit spike (HTTP 429), thousands of concurrent clients may initiate exponential backoff simultaneously.
If all clients calculate pure deterministic exponential backoff ($delay = 2^k$), they will all retry simultaneously at exact identical intervals (e.g. at 2s, 4s, 8s). This concentrated blast of traffic overwhelms the recovering API, causing repeated cascading outages.
**Mitigation:** Adding **Full Jitter** ($delay = \text{Uniform}(0, \min(M, \text{base} \cdot 2^k))$) spreads retry requests uniformly across the timeline, smoothing out the traffic spike and allowing upstream services to recover.

---

## 2. Explain the Three States of a Circuit Breaker and their transitions in a high-concurrency LLM gateway.
**Answer:**
1. **CLOSED**: Normal state. All requests flow directly to the LLM provider. Consecutive errors are counted. If failures exceed `failure_threshold`, the circuit transitions to **OPEN**.
2. **OPEN**: The circuit trips. All incoming requests are immediately fast-failed or redirected to a fallback model/cache without attempting downstream network calls. A cooldown timer starts (`recovery_time_sec`).
3. **HALF_OPEN**: Once the timer elapses, the circuit allows a limited number of probe/canary requests. If they succeed, the circuit returns to **CLOSED**. If any fail, it resets back to **OPEN**.

---

## 3. How do you recognize and solve Binary Search on Answer Space (e.g. LC 1011)?
**Answer:**
Problems that ask for the "minimum capacity", "maximum possible minimum", or "optimal threshold" often have a monotonic feasibility function:
- If capacity $C$ can ship all packages in $D$ days, then any capacity $> C$ can also ship them.
- If capacity $C$ cannot, no capacity $< C$ can.
We binary search over the answer bounds:
- Lower bound: $\max(weights)$ (we must be able to ship the single heaviest item).
- Upper bound: $\sum(weights)$ (shipping everything in 1 day).
For each candidate $mid$, we run a greedy $O(N)$ simulation to check feasibility. Total runtime is $O(N \log(\sum - \max))$, transforming what looks like an exponential search into logarithmic time.
