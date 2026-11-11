# 📝 Notes — Day 23: Capacity & Queueing Theory

- **Tail Latency Explosion:** As utilization $\rho \to 1.0$, latency scales asymptotically as $\frac{1}{1 - \rho}$. Clusters should target $\le 70\%$ steady-state utilization.
- **PriorityBlockingQueue:** Unbounded lock-free / condition-variable heap in `java.util.concurrent`. Never blocks on `offer()`, but blocks on `poll()` when empty.
