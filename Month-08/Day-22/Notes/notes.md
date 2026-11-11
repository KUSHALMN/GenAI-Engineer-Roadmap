# 📝 Notes — Day 22: Pareto Frontier & Concurrency

- **Quantization Gains:** INT4 / AWQ / FP8 can cut memory bandwidth requirements by 50–75% with less than 1.5% drop on quality benchmarks.
- **Semaphore Correctness:** Always release permits in a `finally` block to guarantee permit leaks never occur upon unhandled task exceptions.
