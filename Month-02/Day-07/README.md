# 📅 Day 37 — Month 02, Day 07: Production Reliability

> Build production resilience for LLM applications: exponential backoff retry with full jitter, timeout handling, a fallback-provider chain, and a thread-safe token-bucket rate limiter. Implement Stack, Queue, Deque, and Monotonic Stack in Python and Java.

---

## 📁 Structure

```
Day-07/
├── retry.py                    # Exponential backoff retry with full jitter and exception filtering
├── rate_limiter.py             # Thread-safe Token Bucket rate limiter (RPM/TPM control)
├── fallback_llm.py             # Cascading provider fallback (Primary -> Secondary -> Backup)
├── resilient_llm_service.py    # Integrated service wiring rate limiter + timeout + retry + fallback
├── stack_queue_patterns.py     # LC 20, LC 739 (Monotonic Stack), LC 155 (Min Stack), LC 232
├── README.md
└── DSA/
    └── StackQueuePatterns.java # Java LC 20, LC 739, LC 155 with test cases
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python retry.py
python rate_limiter.py
python fallback_llm.py
python resilient_llm_service.py
python stack_queue_patterns.py
```

### Java Tests
```bash
cd DSA
javac StackQueuePatterns.java
java StackQueuePatterns
```

---

## ✅ Status: Completed
