# Day 10 Notes: Parallel Tool Execution

## 1. Concurrency Mechanics
- Use `concurrent.futures.ThreadPoolExecutor` for IO-bound web API calls.
- Always preserve call index order in output results regardless of which task completes first.
