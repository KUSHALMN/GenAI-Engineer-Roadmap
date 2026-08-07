# Technical Questions — Day 11

## Config Pattern

**Q: Why use a `config.py` file?**
> Centralizes all settings in one place — no hardcoded values scattered across files. To change the model, chunk size, or collection name, you only edit one file. This is the standard pattern in production Python projects.

**Q: What is the difference between hardcoded values and config-driven values?**
> Hardcoded: `model = "llama-3.3-70b-versatile"` scattered in multiple files. Config-driven: defined once in `config.py`, imported everywhere. Config-driven is easier to maintain and change.

**Q: Why use `os.getenv()` instead of hardcoding API keys?**
> Security — API keys should never be in source code. `os.getenv()` reads from environment variables or `.env` files, keeping secrets out of the codebase.

---

## Queue DSA

**Q: What is the difference between Stack and Queue?**
> Stack = LIFO (Last In First Out) — push/pop from same end. Queue = FIFO (First In First Out) — enqueue at back, dequeue from front.

**Q: How does Queue using Two Stacks work?**
> `inbox` stack receives all pushes. When popping/peeking, transfer all elements from inbox to outbox (reversing order). Outbox now serves elements in FIFO order. Transfer only happens when outbox is empty — amortized O(1).

**Q: What is a sliding window queue?**
> A queue that maintains elements within a fixed time/size window. In Number of Recent Calls, we keep only pings within the last 3000ms by removing old entries from the front.

**Q: When to use Queue vs Stack?**
> Queue: BFS, task scheduling, sliding window, rate limiting. Stack: DFS, bracket matching, undo operations, expression evaluation.
