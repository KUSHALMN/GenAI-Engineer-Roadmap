# Day 20: Technical Interview Preparation — Continuous Batching & ThreadPools

### Q1: Why does Continuous Batching (Iteration-Level Batching) yield $2\times - 4\times$ higher throughput than Static Batching?
**Answer:**
In static batching, all requests in a batch must wait until the slowest/longest sequence finishes generation, leaving GPU compute slots idle for shorter completed sequences (padding waste). Continuous batching operates at the iteration granularity: as soon as a sequence emits `<EOS>`, its slot and KV cache are freed, and a waiting request from the queue enters the batch on the very next step.

### Q2: What is the difference between `executor.execute()` and `executor.submit()` in Java?
**Answer:**
- `execute(Runnable)`: Fires-and-forgets a task with void return; unhandled exceptions bubble to the thread's uncaught exception handler.
- `submit(Callable/Runnable)`: Returns a `Future` object allowing the caller to obtain the return value or catch thrown exceptions via `future.get()`.
