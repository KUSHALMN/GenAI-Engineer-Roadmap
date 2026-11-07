# Month 05 — Day 17: Inference vs Training Deep Dive

## Objectives
1. **GenAI:** Model compute-bound prefill vs memory-bound decode latency dynamics.
2. **DSA:** Implement lock-free multi-threaded metric aggregation with `ConcurrentHashMap` in Java.

## Repository Layout
```
Day-17/
├── AI/
│   └── prefill_decode_benchmark.py
├── DSA/
│   └── ConcurrentStateMap.java
├── Interview/
│   └── technical_questions.md
├── Notes/
│   └── notes.md
└── README.md
```

## How to Run

### Python AI Implementation:
```bash
python Month-05/Day-17/AI/prefill_decode_benchmark.py
```

### Java DSA Solution:
```bash
javac Month-05/Day-17/DSA/ConcurrentStateMap.java
java -cp Month-05/Day-17/DSA ConcurrentStateMap
```
