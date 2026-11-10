# 🎯 Technical Interview Questions — Day 07: Object Storage & Transactions

### 1. Why should direct user uploads go through S3 Pre-Signed URLs instead of streaming through your API server?
**Answer:**
Streaming multi-megabyte/gigabyte uploads directly through application web servers saturates API threads, spikes server memory/bandwidth, and risks network timeouts. Pre-signed URLs offload network I/O directly to AWS S3/Cloud Storage edge endpoints, while maintaining strict IAM permissions, content-type locks, and temporary expirations.

### 2. Explain Dirty Reads, Non-Repeatable Reads, and Phantom Reads across SQL Isolation Levels.
**Answer:**
- **Dirty Read:** Transaction A reads uncommitted changes from Transaction B. Prevented by `READ COMMITTED`.
- **Non-Repeatable Read:** Transaction A re-reads the same row and sees modified data because Transaction B committed an update. Prevented by `REPEATABLE READ`.
- **Phantom Read:** Transaction A re-runs a range query and sees new rows inserted by Transaction B. Prevented by `SERIALIZABLE`.
