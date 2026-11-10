# 🎯 Technical Interview Questions — Day 14: Canary Releases & Allocation

### 1. Contrast Blue-Green Deployments with Canary Deployments in production AI systems.
**Answer:**
- **Blue-Green:** Two identical production environments. The router instantaneously switches 100% of user traffic from Blue (idle) to Green (new). Zero downtime, but requires 2x GPU hardware infrastructure.
- **Canary:** Gradually shifts a small fraction of traffic (e.g., 5% -> 25% -> 100%) to the new version while evaluating P99 latency and error rates. Much safer for large LLM updates where prompt regressions could impact users.

### 2. How does Escape Analysis allow the JVM to avoid heap allocation?
**Answer:**
If the JIT compiler determines that an object allocated inside a method never escapes the method's scope (i.e., it is neither returned nor assigned to a global reference), the JVM can perform **Scalar Replacement**, allocating its fields directly onto CPU registers or the thread call stack instead of the heap.
