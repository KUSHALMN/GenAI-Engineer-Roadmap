# Day 23 Notes: Model Server Concurrency

## 1. Concurrency Bottlenecks
- Beyond GPU KV capacity, requests enter a pending FIFO queue, linearly increasing Time-To-First-Token.
