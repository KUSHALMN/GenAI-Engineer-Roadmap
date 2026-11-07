# Day 28: Technical Interview Preparation — Capacity Planning & Java Memory Model

### Q1: Why is `volatile` strictly required in Double-Checked Locking under the Java Memory Model?
**Answer:**
Without `volatile`, the instruction sequence `instance = new Singleton()` can be reordered by the JVM compiler into:
1. Allocate memory.
2. Assign pointer to `instance` (non-null).
3. Execute constructor.
If thread B checks `instance == null` between steps 2 and 3, it sees a non-null reference and accesses an uninitialized object. The `volatile` modifier establishes a happens-before relationship, prohibiting instruction reordering across the write barrier.

### Q2: How do you plan capacity when user queries spike $10\times$ during business hours?
**Answer:**
1. **Auto-scaling GPU Nodes:** Use Kubernetes (KEDA) to scale model replicas based on queue depth.
2. **Dynamic Speculative Decoding:** Trade compute for latency during peak hours.
3. **Semantic Caching:** Cache popular prompt embeddings to deflect 20-30% of traffic before reaching GPUs.
