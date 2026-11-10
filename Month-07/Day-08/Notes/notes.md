# 📝 Notes — Day 08: Background Queues & SQL Mastery

## 1. Queue Architecture Best Practices
- **Dead-Letter Queue (DLQ):** Poison-pill messages that crash workers repeatedly must be quarantined to DLQs to prevent blocking healthy messages.
- **Visibility Timeout:** While a worker processes a message, the message is hidden from other workers. If the worker dies before `ack`, the visibility timeout expires and the message is re-queued.
