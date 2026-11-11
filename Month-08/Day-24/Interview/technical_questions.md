# 🎯 Technical Interview Questions — Day 24: Chaos Testing & Hard DSA Mock A

## Question 1: How do you design chaos engineering experiments for LLM microservices to validate resilience against cascade outages?
**Answer:**
1. **Fault Injection Vectors:**
   - **Network Latency Injection (P99 spikes):** Artificially inject 5,000ms delay to verify downstream client timeout budgets and thread-pool isolation.
   - **Provider 429 Quota Exhaustion:** Inject HTTP 429 status codes with `Retry-After` headers to validate exponential backoff with jitter and secondary provider routing.
   - **Context Window Truncation / Malformed Payloads:** Inject corrupted JSON tokens to test parser error handling and schema fallbacks.
2. **Circuit Breaker Verification:** Verify that after 5 consecutive failures, the breaker trips to `OPEN`, immediately serving cached responses or degraded models without stressing the upstream provider.

---

## Question 2: In LeetCode 42 (Trapping Rain Water), prove why the two-pointer approach works without scanning leftMax and rightMax globally.
**Answer:**
- Water trapped above bar $i$ depends strictly on $\min(\max_{\text{left}}, \max_{\text{right}}) - height[i]$.
- In the two-pointer approach, if `height[left] < height[right]`, we know with certainty that the global maximum to the right of `left` is at least `height[right]` (and thus $\ge leftMax$).
- Therefore, the bottleneck for `left` is solely determined by `leftMax`. We can safely record trapped water at `left` and advance `left++`. The symmetric logic applies when `height[right] <= height[left]`.
