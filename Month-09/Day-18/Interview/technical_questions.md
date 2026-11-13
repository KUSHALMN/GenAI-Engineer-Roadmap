# 🎯 Technical Interview Questions — Day 18: Fault Tolerance & Burst Balloons

## Question 1: How do modern frameworks (PyTorch TorchElastic / torchrun) handle hardware node failures without terminating the entire pretraining run?
**Answer:**
1. **Rendezvous Backend (etcd / c10d):** Workers register heartbeats with a central rendezvous controller. When a GPU server crashes or hangs, heartbeat timeouts detect the failure within seconds.
2. **Dynamic Process Group Re-establishment:** The rendezvous system evicts the failed node, spawns a warm spare instance, and triggers a clean re-rendezvous across the remaining ranks.
3. **Rollback to Last Async Checkpoint:** The cluster loads the latest PyTorch Distributed Checkpoint (DCP) from shared storage and resumes pretraining, achieving zero manual operator intervention and bounding lost progress to $< 100$ steps.

---

## Question 2: In LeetCode 312 (Burst Balloons), why does working from the LAST balloon burst make subproblems independent, whereas the first balloon burst fails?
**Answer:**
- **The Dependency Dilemma:** If we choose balloon $k$ to burst *first*, balloons $k-1$ and $k+1$ become adjacent, dynamically altering the multipliers for all subsequent bursts and coupling subproblems.
- **The "Last Burst" Insight:** If we instead select balloon $k$ as the *last* balloon to burst in interval $[left, right]$, the boundary balloons ($left-1$ and $right+1$) remain completely intact throughout all earlier bursts in both sub-intervals $[left, k-1]$ and $[k+1, right]$.
- Thus, the subproblems $[left, k-1]$ and $[k+1, right]$ become completely decoupled and independent, allowing classical $O(N^3)$ interval dynamic programming.
