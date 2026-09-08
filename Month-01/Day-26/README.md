# 📅 Day 26: 🛡️ Error Handling + Guardrails & Merge k Sorted Lists DSA

Welcome to **Day 26** of the **GenAI Engineer Roadmap**! Today focuses on building production-grade GenAI guardrails, input/output safety filters, PII redaction, exponential backoff with full jitter, model fallback cascades, and mastering LeetCode 23 (Merge k Sorted Lists) in Java.

---

## 📁 Day 26 Project Structure

```
Day-26/
├── AI/
│   └── guardrails-api/
│       ├── src/
│       │   ├── guardrails.py       # Jailbreak detection, toxic blockers, PII redaction
│       │   ├── resilience.py       # Exponential backoff with jitter & model fallback cascade
│       │   └── app.py              # FastAPI gateway with multi-tier validation
│       ├── tests/
│       │   └── test_guardrails.py  # Guardrail blocking, PII masking & fallback failover tests
│       ├── requirements.txt
│       └── README.md
│
├── src/
│   ├── guardrails.py
│   ├── resilience.py
│   └── app.py
├── tests/
│   └── test_guardrails.py
│
├── DSA/
│   └── merge_k_sorted_lists.java   # LeetCode 23: Merge k Sorted Lists (Min-Heap & Divide-and-Conquer)
│
├── Interview/
│   ├── technical_questions.md       # Thundering herd, full jitter, model fallbacks
│   ├── coding_questions.md          # PriorityQueue O(N log k) invariants
│   └── recruiter_questions.md       # Defense-in-depth security talking points
│
├── Notes/
│   └── day26_notes.md
├── Resources.md
└── README.md
```

---

## ⚡ Core Concepts Learned

1. **Input & Output Guardrails**: Symmetric validation rejecting jailbreak heuristics and toxic prompts while scrubbing PII.
2. **Exponential Backoff with Full Jitter**: Dispersing retry traffic across time to survive rate limits.
3. **Multi-Model Fallback Cascades**: Automatic failover from primary frontier models to lightweight backups.
4. **Merge k Sorted Lists**: Optimal Min-Heap PriorityQueue execution in Java.

---

## 🚀 Execution Commands

### Test Guardrails & Fallback Suite
```bash
python -m pytest Month-01/Day-26/tests/test_guardrails.py -v
```

### Run Merge k Sorted Lists Java Solution
```bash
javac Month-01/Day-26/DSA/merge_k_sorted_lists.java
java -cp Month-01/Day-26/DSA merge_k_sorted_lists
```
