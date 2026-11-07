# Day 27 Notes: Inference Failure Handling

## 1. Failure Modes
- Context Overflow -> Intelligent Truncation / Summarization.
- HTTP 429 -> Exponential Jitter Backoff.
- GPU OOM -> Request Preemption & Eviction.
