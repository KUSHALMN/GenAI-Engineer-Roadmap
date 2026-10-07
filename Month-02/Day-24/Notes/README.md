# 📅 Day 24 — Month 02: GenAI Observability & Tracing Architecture

> Build a production-grade observability and tracing system for LLMs and RAG pipelines, featuring structured JSON logging, distributed `request_id` propagation, latency percentiles (p50/p95/p99), and real-time token cost computation. Implement Monotonic Stack and Queue patterns (LC 239, 739, 496) in Java.

---

## 📁 Architecture Overview

```
Day-24/
├── AI/
│   ├── observability/
│   │   ├── logger.py            # Structured JSON logger with request context
│   │   ├── request_id.py        # ContextVars request ID propagation
│   │   ├── latency.py           # Execution timers & checkpoint spans
│   │   ├── metrics.py           # Percentile & error rate aggregator
│   │   └── cost_tracker.py      # Token cost calculator across models
│   ├── rag/
│   │   └── observable_rag.py    # Fully instrumented RAG pipeline
│   └── logs/
│       └── sample_log.json      # Structured trace payload sample
├── Java/
│   └── MonotonicQueueStack.java # LC 239 + LC 739 + LC 496 (Java)
├── DSA/
│   └── MonotonicQueueStack.java # Alternate DSA reference
├── Interview/
│   └── technical_questions.md   # System design & algorithm Q&A
├── Notes/
│   ├── notes.md                 # Deep-dive study notes
│   └── README.md                # Day documentation copy
└── README.md
```

---

## 🚀 Execution & Verification

### 1. Test Observable RAG Pipeline (Python in `AI/`)
```bash
python Month-02/Day-24/AI/rag/observable_rag.py
```

### 2. Compile & Run Java DSA Suite (in `Java/`)
```bash
cd Month-02/Day-24/Java
javac MonotonicQueueStack.java && java MonotonicQueueStack
```
