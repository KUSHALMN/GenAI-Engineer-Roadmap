# 📅 Day 30: 🏗️ GenAI System Design & Search Autocomplete DSA

Welcome to **Day 30** of the **GenAI Engineer Roadmap**! Today focuses on designing high-scale, multi-tenant Generative AI platforms: dual Token Bucket rate limiting (RPM + TPM), intelligent model routing, PagedAttention serving architectures, cost control telemetry, and mastering LeetCode 642 (Search Autocomplete System) in Java.

---

## 📁 Day 30 Project Structure

```
Day-30/
├── AI/
│   └── system-design-gateway/
│       ├── src/
│       │   ├── rate_limiter.py     # Dual RPM + TPM Token Bucket rate limiter
│       │   ├── router.py           # Complexity-aware dynamic model router
│       │   └── app.py              # FastAPI enterprise gateway with tenant quotas
│       ├── tests/
│       │   └── test_gateway.py     # Quota enforcement, burst allowance & routing tests
│       ├── requirements.txt
│       └── README.md
│
├── src/
│   ├── rate_limiter.py
│   ├── router.py
│   └── app.py
├── tests/
│   └── test_gateway.py
│
├── DSA/
│   └── search_autocomplete.java    # LeetCode 642: Search Autocomplete System (Trie + PriorityQueue)
│
├── Interview/
│   ├── technical_questions.md       # Multi-tenant 10k RPS architecture, PagedAttention
│   ├── coding_questions.md          # Trie frequency caching & Min-Heap ranking
│   └── recruiter_questions.md       # Self-hosting vs proprietary API trade-offs
│
├── Notes/
│   └── day30_notes.md
├── Resources.md
└── README.md
```

---

## ⚡ Core Concepts Learned

1. **Dual Token Bucket Quotas**: Restricting both request bursts (RPM) and token budgets (TPM) per tenant.
2. **Dynamic Model Routing**: Slashing API bills by matching prompt complexity to model tier.
3. **High-Throughput Serving**: PagedAttention, continuous batching, and KV-cache optimization.
4. **Search Autocomplete DSA**: Prefix-tree navigation with real-time frequency scoring.

---

## 🚀 Execution Commands

### Test GenAI System Design Gateway
```bash
python -m pytest Month-01/Day-30/tests/test_gateway.py -v
```

### Run Search Autocomplete Java Solution
```bash
javac Month-01/Day-30/DSA/search_autocomplete.java
java -cp Month-01/Day-30/DSA search_autocomplete
```
