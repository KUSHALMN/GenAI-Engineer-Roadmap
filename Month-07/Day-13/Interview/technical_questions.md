# 🎯 Technical Interview Questions — Day 13: CI Pipelines & Java Reflection

### 1. How does a Continuous Integration (CI) pipeline for GenAI systems differ from traditional software CI?
**Answer:**
Traditional CI focuses on determinism (linting, compiling, unit tests with 100% predictable inputs). GenAI CI requires additional non-deterministic evaluation steps:
- **Evaluation against Golden Datasets:** Measuring semantic similarity, NDCG, and hallucination rates.
- **Safety & Prompt Injection Tests:** Fuzzing inputs with red-team jailbreaks to detect model drift.
- **Cost & Latency Thresholds:** Ensuring prompt template updates do not exceed token budgets.

### 2. What are the performance and security trade-offs of Java Reflection?
**Answer:**
- **Performance:** Reflection inspects class metadata at runtime and bypasses JVM inlining and JIT compiler optimizations, introducing CPU overhead.
- **Security:** Reflection can access private fields (`setAccessible(true)`), potentially violating encapsulation and security sandbox invariants.
