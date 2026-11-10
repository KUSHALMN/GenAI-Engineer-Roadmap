# 🎯 Technical Interview Questions — Day 26: Agent Runtimes & Ring Buffers

### 1. How do you design crash recovery for long-running stateful AI agents?
**Answer:**
Treat agent execution as a state machine where every step (thought, tool call, tool observation) is committed to persistent storage (PostgreSQL/Redis) before taking action. If a worker pod crashes, the newly spawned pod reloads the state snapshot from the database and resumes from the last uncommitted step with exact idempotency.

### 2. How do explicit `Condition` variables compare with Java's intrinsic `wait()` / `notify()`?
**Answer:**
A single intrinsic object lock supports only one wait-set. `ReentrantLock` allows creating multiple distinct conditions (e.g., `notFull` and `notEmpty`). This avoids waking up consumer threads when only producers need to be notified, completely eliminating CPU thrashing from redundant thread wakeups.
