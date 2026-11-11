# 🎯 Technical Interview Questions — Day 23: Capacity Queueing & Priority Dispatchers

## Question 1: How does Little's Law ($L = \lambda W$) govern LLM inference clusters?
**Answer:**
- **Mathematical Form:** In any stable queueing system, the average number of concurrent requests in the system ($L$) equals the long-term average arrival rate ($\lambda$) multiplied by the average time a request spends in the system ($W$).
- **Application to GPU Memory:** If $\lambda = 200\text{ rps}$ and average generation latency $W = 1.5\text{ seconds}$, the cluster must support $L = 200 \times 1.5 = 300$ active concurrent requests at all times.
- **KV Cache Dimensioning:** Each concurrent generation holds an active KV cache in GPU HBM ($L \times \text{Context Size} \times \text{Layer Memory}$). Sizing GPU memory without considering Little's Law leads to sudden out-of-memory (OOM) evictions during traffic bursts.

---

## Question 2: How do you design an unbounded priority queue that guarantees zero starvation for low-priority tasks?
**Answer:**
- **Dynamic Priority Aging:** When a task waits in queue, its effective priority increases as a function of time:
  $$\text{Effective Priority} = P_{\text{base}} + \alpha \times (t_{\text{current}} - t_{\text{entry}})$$
- **Multi-Level Feedback Queues (MLFQ):** Alternatively, maintain discrete priority buckets (Critical, High, Default, Low) and service them using Deficit Round Robin (DRR) or Weighted Fair Queueing (WFQ) with proportional time quantum allotments.
