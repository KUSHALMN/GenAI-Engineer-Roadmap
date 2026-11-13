# 📝 Notes — Day 18: Fault Tolerance & Interval DP

- **Straggler Mitigation:** A single thermal-throttling GPU stalls the entire cluster in synchronous All-Reduce; straggler detectors flag and drain offending nodes automatically.
- **Virtual Balloon Boundaries:** Array padding with `arr[0] = 1` and `arr[n+1] = 1` simplifies edge boundary cases to zero.
