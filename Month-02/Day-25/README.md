# 📅 Day 25 — Month 02: Production LLM Reliability & Resilient Async Systems

> Build an enterprise-grade reliability harness for GenAI services: Exponential Backoff with Full Jitter, Token Bucket Rate Limiting, Three-State Circuit Breakers, Call Timeouts, and Provider Fallbacks. Master Advanced Binary Search patterns (LC 33, 153, 1011) in Java.

---

## 📁 Architecture Overview

```
Day-25/
├── reliability/
│   ├── retry.py             # Retry loop with exponential backoff
│   ├── backoff.py           # Jittered exponential delay algorithm
│   ├── timeout.py           # Synchronous & asynchronous timeout guards
│   ├── rate_limiter.py      # Token Bucket algorithm for quota enforcement
│   ├── circuit_breaker.py   # Closed/Open/Half-Open state machine
│   └── fallback.py          # Cascading multi-provider failover router
├── async/
│   └── async_llm.py         # Async resilient LLM client with batch generation
├── DSA/
│   └── BinarySearchAdvanced.java # LC 33 + LC 153 + LC 1011 (Java)
├── Interview/
│   └── technical_questions.md # Distributed systems & algorithms Q&A
├── Notes/
│   └── notes.md             # Theoretical deep-dive
└── README.md
```

---

## 🚀 Execution & Verification

### 1. Test Resilient Async LLM (Python)
```bash
python Month-02/Day-25/async/async_llm.py
```

### 2. Compile & Run Java DSA Suite
```bash
cd Month-02/Day-25/DSA
javac BinarySearchAdvanced.java && java DSA.BinarySearchAdvanced
```
