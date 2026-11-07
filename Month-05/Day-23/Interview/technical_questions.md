# Day 23: Technical Interview Preparation — Server Concurrency & Deadlocks

### Q1: What are the four Coffman conditions required for a deadlock to occur?
**Answer:**
1. **Mutual Exclusion:** Resources cannot be shared simultaneously.
2. **Hold and Wait:** A process holds one resource while waiting for another.
3. **No Preemption:** Resources cannot be forcibly taken away.
4. **Circular Wait:** A closed chain of processes exists where each process holds a resource needed by the next.
*Fix:* Breaking *Circular Wait* via strict global lock acquisition ordering eliminates deadlocks.

### Q2: What happens when an LLM server's concurrency exceeds its KV cache memory limit?
**Answer:**
The server experiences Out-Of-Memory (OOM) or must preempt (evict/swap) active requests. PagedAttention engines preempt the lowest-priority active sequence, evicting its pages to CPU RAM and re-computing or swapping them back when GPU slots reopen.
