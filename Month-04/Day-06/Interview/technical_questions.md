# Day 06: Technical Interview Preparation — Stateful Agent Design

### Q1: Why is immutable state (e.g., using frozen dataclasses / LangGraph state reducers) preferred over mutable shared state in multi-step agents?
**Answer:**
1. **Traceability and Time-Travel Debugging:** Immutable state creates an append-only snapshot at every step, making it trivial to rewind, replay, or inspect agent reasoning history.
2. **Concurrency Safety:** Multiple subagents or async parallel tool dispatchers can read state without race conditions or locks.
3. **Idempotent Checkpointing:** Serializing an immutable object to Redis or PostgreSQL cannot be corrupted by background threads mutating objects mid-write.

### Q2: How do diagonal indices `r - c + n` and `r + c` uniquely identify diagonals on a chessboard?
**Answer:**
- On any main diagonal (top-left to bottom-right), the difference between row and column `r - c` is constant. Adding `n` shifts negative differences to positive values for 0-indexed arrays.
- On any anti-diagonal (top-right to bottom-left), the sum of row and column `r + c` is constant. Both have at most $2n - 1$ unique diagonals.
