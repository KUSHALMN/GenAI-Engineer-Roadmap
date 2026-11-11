# 🎯 Technical Interview Questions — Day 31: Platform Benchmarking & Lock-Free Data Structures

## Question 1: How do lock-free data structures using Compare-And-Swap (CAS) outperform synchronized locks in multi-threaded systems?
**Answer:**
1. **Lock-Free Guarantees:** Lock-free algorithms guarantee that at least one thread makes progress in a finite number of steps, eliminating deadlocks, priority inversion, and OS thread context switching overhead.
2. **CAS Hardware Primitives:** CAS (`CMPXCHG` on x86) operates directly at the CPU cache-coherency bus level. An update only commits if the expected memory address has not changed; otherwise, it retries in a tight spin loop.
3. **ABA Mitigation:** In garbage-collected runtimes like Java, node memory is not immediately recycled into arbitrary types while references remain reachable, mitigating the classic ABA memory reuse bug.

---

## Question 2: What benchmarking metrics define a production-grade LLM inference gateway?
**Answer:**
- **Time to First Token (TTFT):** Measures prompt processing speed (prefill phase); critical for human perception of responsiveness.
- **Inter-Token Latency (ITL) / Generation Time per Token:** Measures decode phase bandwidth.
- **Tail Latency Distributions (P95, P99, P99.9):** Identifies GC pauses, GPU queue contention, and network jitter.
- **Goodput vs Throughput:** Request count that not only completes, but strictly satisfies the target SLO latency envelope ($L \le \text{SLO}$).
