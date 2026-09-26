# 📅 Day 47 — Month 02, Day 17: Advanced Inference Optimization

> Build a generation latency benchmark, an inter-token latency & TTFT telemetry calculator, a dynamic continuous batching simulator demonstrating KV cache memory overhead, and an architectural report on precision formats (FP16/BF16/INT8/INT4) and speculative decoding. Implement Backtracking patterns in Python and Java.

---

## 📁 Structure

```
Day-17/
├── latency_metrics.py          # TTFT, ITL, and tokens/sec telemetry tracker
├── inference_benchmark.py      # Streaming generation benchmark across prompt contexts
├── batch_inference.py          # Continuous batching simulator & KV-cache memory sizing
├── optimization_report.md      # Precision tradeoffs, memory bandwidth bounds, speculative decoding
├── backtracking.py             # Subsets, Permutations, Combinations, Word Search, N-Queens
├── README.md
└── DSA/
    └── BacktrackingPatterns.java # Backtracking patterns in Java (LC 78, LC 46, LC 51)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python latency_metrics.py
python inference_benchmark.py
python batch_inference.py
python backtracking.py
```

### Java Tests
```bash
cd DSA
javac BacktrackingPatterns.java
java BacktrackingPatterns
```

---

## ✅ Status: Completed
