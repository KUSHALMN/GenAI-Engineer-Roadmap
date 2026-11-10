# 🎯 Technical Interview Questions — Day 09: Docker & Concurrency

### 1. Why are multi-stage Docker builds critical for production AI systems?
**Answer:**
Compiling Python C-extensions (e.g., PyTorch, tokenizers, or llama-cpp) requires heavy build tools (`gcc`, `g++`, `make`, header files). Multi-stage builds compile artifacts in an ephemeral builder image and copy only the final binaries/wheels into a minimal distroless or alpine runtime image. This reduces image size from ~3GB to <250MB, speeding up CI deployment and shrinking the attack surface.

### 2. How does `CountDownLatch` differ from `CyclicBarrier` in Java?
**Answer:**
- `CountDownLatch`: A one-time synchronization barrier where one or more threads wait until a set of operations being performed in other threads completes (`countDown()`). It cannot be reset.
- `CyclicBarrier`: A reusable barrier where all participant threads wait for each other to reach a common barrier point before proceeding.
