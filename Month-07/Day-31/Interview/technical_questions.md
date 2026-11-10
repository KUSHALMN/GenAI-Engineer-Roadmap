# 🎯 Technical Interview Questions — Day 31: Lock-Free Queues & Benchmarks

### 1. How does the Michael-Scott Non-Blocking Queue achieve thread-safety without locks?
**Answer:**
The Michael-Scott queue uses **AtomicReference** and hardware-supported **Compare-And-Swap (CAS)** operations. In `enqueue()`, a thread attempts to swing the `tail.next` pointer from null to the new node via CAS. If another thread beat it, it assists the rival thread by advancing the `tail` pointer and retries in a loop, guaranteeing lock-free progress without thread suspension.

### 2. What is the difference between Latency and Throughput under high concurrency?
**Answer:**
- **Throughput:** The volume of completed transactions per unit time (e.g., 2,500 requests/sec).
- **Latency:** The elapsed duration to complete a single transaction (e.g., P99 = 45ms).
As concurrency increases beyond server saturation capacity, queuing delay increases exponentially (Little's Law), causing P99 latency to degrade dramatically even if throughput plateaus.
