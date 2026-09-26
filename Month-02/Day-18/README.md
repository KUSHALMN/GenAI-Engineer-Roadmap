# 📅 Day 48 — Month 02, Day 18: Model Routing & Adaptation

> Build a rule-based model router (small vs large model dynamic delegation), an abstract provider interface, a resilient fallback router with circuit-breaker tracking, and an adaptation decision matrix comparing prompting, RAG, and fine-tuning. Implement 1D Dynamic Programming patterns in Python and Java.

---

## 📁 Structure

```
Day-18/
├── provider_interface.py       # Abstract Base Class LLMProvider and mock implementations
├── model_router.py             # Small vs Large model routing based on query complexity
├── fallback_router.py          # Cascading failover router across provider backends
├── adaptation_decision.md      # Decision matrix: Prompting vs RAG vs Fine-Tuning
├── dp_1d.py                    # Climbing Stairs, House Robber, Coin Change, LIS (LC 70, 198, 322, 300)
├── README.md
└── DSA/
    └── DynamicProgramming1D.java # 1D DP in Java (LC 70, LC 198, LC 322)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python provider_interface.py
python model_router.py
python fallback_router.py
python dp_1d.py
```

### Java Tests
```bash
cd DSA
javac DynamicProgramming1D.java
java DynamicProgramming1D
```

---

## ✅ Status: Completed
