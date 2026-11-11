# 📝 Notes — Day 31: Platform Benchmarking & Lock-Free Structures

- **Treiber Stack Progress Invariant:** Even under extreme thread contention, at least one thread succeeds in executing `top.compareAndSet(...)` on every attempt.
- **Goodput Optimization:** Rejecting or degrading queries early yields higher overall system goodput than allowing queues to saturate HBM memory.
