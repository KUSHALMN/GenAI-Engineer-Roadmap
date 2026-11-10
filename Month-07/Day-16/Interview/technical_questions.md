# 🎯 Technical Interview Questions — Day 16: Rate Limiting & Elevator LLD

### 1. Compare the Token Bucket vs. Leaky Bucket vs. Sliding Window Counter algorithms.
**Answer:**
- **Token Bucket:** Tokens replenish at a fixed rate up to a burst capacity. Allows sudden bursts of traffic while enforcing average rate.
- **Leaky Bucket:** Requests enter a buffer and leak out at a strictly uniform rate. Eliminates bursts and guarantees constant throughput (ideal for traffic shaping).
- **Sliding Window Counter:** Divides the rate window into discrete sub-windows (e.g., 10-second segments) to calculate weighted request counts, eliminating boundary reset spikes.

### 2. How do you model real-world elevator dispatching (e.g., SCAN/LOOK algorithm)?
**Answer:**
Maintain two sorted sets of destination requests (`upRequests` in ascending order, `downRequests` in descending order). The elevator continues serving requests in the current direction until the set is empty, then reverses direction (LOOK algorithm), preventing starvation and minimizing mechanical wear.
