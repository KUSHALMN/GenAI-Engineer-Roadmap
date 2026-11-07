# Day 18: Technical Interview Preparation — Quantization & Bounded Blocking Queue

### Q1: Compare AWQ (Activation-Aware Weight Quantization) vs GPTQ.
**Answer:**
- **AWQ:** Observes that not all weights are equally important; protecting the top 1% salient weights based on activation magnitudes preserves accuracy without costly per-layer matrix regressions. High generalizability and faster calibration.
- **GPTQ:** Uses second-order Taylor expansion (Hessian matrix) to greedily quantize weights while adjusting remaining unquantized weights to compensate for error. Higher compute required during calibration.

### Q2: Why is `while (count == elements.length)` used instead of `if` before `await()`?
**Answer:**
To protect against spurious wakeups (where a thread wakes without a signal) and race conditions where multiple threads wake up simultaneously but only one thread successfully acquires the lock and finds an open slot. Re-evaluating the condition inside a `while` loop guarantees correctness.
