# 🎯 Technical Interview Questions — Day 25: RAG Probes & Immutability

### 1. Explain the distinction between Kubernetes Liveness, Readiness, and Startup Probes in LLM services.
**Answer:**
- **Startup Probe:** Checks if the container has finished its slow initialization (e.g., downloading 15GB weights into GPU VRAM). Disables liveness/readiness checks until it passes.
- **Liveness Probe:** Checks if the process is alive (not deadlocked). If it fails, Kubernetes kills and restarts the pod.
- **Readiness Probe:** Checks if the service is ready to accept incoming user traffic (e.g., vector index loaded). If it fails, Kubernetes temporarily removes the pod from the Load Balancer endpoints without restarting it.

### 2. Why are defensive copies critical when returning collections from domain models?
**Answer:**
Returning a direct reference to an internal mutable collection allows external callers to modify the class's internal state directly (e.g., `policy.getScopes().clear()`), violating class invariants and leading to severe concurrency race conditions.
