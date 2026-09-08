# 📅 Day 27: 🔍 LLM Observability & Median of Two Sorted Arrays DSA

Welcome to **Day 27** of the **GenAI Engineer Roadmap**! Today focuses on building production-grade LLM observability, distributed tracing with OpenTelemetry spans, latency percentiles ($p50, p95, p99$), real-time token accounting, dollar cost tracking, and mastering LeetCode 4 (Median of Two Sorted Arrays) in Java.

---

## 📁 Day 27 Project Structure

```
Day-27/
├── AI/
│   └── observability-tracer/
│       ├── src/
│       │   ├── tracer.py           # Context manager span tracer, cost calculator, percentiles
│       │   └── app.py              # FastAPI service with /metrics and /traces endpoints
│       ├── tests/
│       │   └── test_observability.py # Span lifecycle, token counts & percentile verification
│       ├── requirements.txt
│       └── README.md
│
├── src/
│   ├── tracer.py
│   └── app.py
├── tests/
│   └── test_observability.py
│
├── DSA/
│   └── median_two_sorted_arrays.java # LeetCode 4: Median of Two Sorted Arrays (Binary Search Partition)
│
├── Interview/
│   ├── technical_questions.md       # Latency percentiles vs averages, cost attribution
│   ├── coding_questions.md          # Binary search on partition invariants
│   └── recruiter_questions.md       # Operational telemetry & cost optimization
│
├── Notes/
│   └── day27_notes.md
├── Resources.md
└── README.md
```

---

## ⚡ Core Concepts Learned

1. **Distributed Tracing**: Capturing spans across gateway, retrieval, and LLM inference.
2. **Percentile Latency ($p50, p95, p99$)**: Accurately assessing long-tail autoregressive decode time.
3. **Unit Cost Economics**: Real-time dollar tracking per model and per tenant.
4. **Binary Search on Partition**: Achieving $O(\log(\min(m, n)))$ optimal time on sorted arrays.

---

## 🚀 Execution Commands

### Test Observability Telemetry Suite
```bash
python -m pytest Month-01/Day-27/tests/test_observability.py -v
```

### Run Median of Two Sorted Arrays Java Solution
```bash
javac Month-01/Day-27/DSA/median_two_sorted_arrays.java
java -cp Month-01/Day-27/DSA median_two_sorted_arrays
```
