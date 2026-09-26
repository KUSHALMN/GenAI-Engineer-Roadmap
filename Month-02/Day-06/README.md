# 📅 Day 36 — Month 02, Day 06: LLM Observability & Debugging

> Add structured JSON logging with request/session context propagation, fine-grained span and TTFT latency tracking, an automated observability middleware, and a metrics summary generator. Implement Sliding Window DSA patterns in Python and Java.

---

## 📁 Structure

```
Day-06/
├── logging.py                  # Structured JSON formatter with contextvars propagation
├── latency_tracker.py          # Sub-millisecond span timing, TTFT, and p50/p90/p95/p99 metrics
├── observability_middleware.py # Request tracer & decorator capturing tokens and spans
├── metrics_report.py           # Telemetry aggregator for throughput, SLAs, and costs
├── sliding_window.py           # Sliding Window DSA in Python (LC 3, 209, 643, 76)
├── README.md
└── DSA/
    └── SlidingWindow.java      # Sliding Window in Java (LC 3, LC 209, LC 643)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python logging.py
python latency_tracker.py
python observability_middleware.py
python metrics_report.py
python sliding_window.py
```

### Java Tests
```bash
cd DSA
javac SlidingWindow.java
java SlidingWindow
```

---

## ✅ Status: Completed
