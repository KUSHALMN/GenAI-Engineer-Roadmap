# 🎯 Technical Interview Questions — Day 08: Background Queues & SQL

### 1. How do you guarantee At-Least-Once vs. Exactly-Once processing in Celery / SQS / Kafka pipelines?
**Answer:**
- **At-Least-Once Delivery:** The message broker ensures delivery, but network partitions or worker crashes before sending an acknowledgment (`ack`) can cause redelivery.
- **Exactly-Once Semantics (EOS):** Requires pairing At-Least-Once transport with **Idempotent Consumers**. By generating a deterministic idempotency key (e.g., `hash(tenant_id + document_id + version)`), the worker checks Redis or a PostgreSQL unique constraint before execution.

### 2. Compare `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()` in SQL.
**Answer:**
- `ROW_NUMBER()`: Always assigns distinct sequential integers (1, 2, 3, 4) regardless of ties.
- `RANK()`: Assigns the same rank to ties, but skips the next rank numbers (1, 2, 2, 4).
- `DENSE_RANK()`: Assigns the same rank to ties without skipping subsequent numbers (1, 2, 2, 3).
