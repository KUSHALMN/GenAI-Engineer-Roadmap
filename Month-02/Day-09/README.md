# 📅 Day 39 — Month 02, Day 09: Guardrails & Safe AI Execution

> Build an input guardrail layer, PII detection and redaction demo, schema-based structured output validation, Human-in-the-Loop (HITL) tool approval, and an agent loop max-iteration safety guard. Implement singly linked list operations in Python and Java.

---

## 📁 Structure

```
Day-09/
├── input_guardrail.py          # Input policy checking, length and topic safety enforcement
├── pii_detector.py             # Regex & reversible pseudonymization for PII entities
├── output_guardrail.py         # JSON schema extractor and field constraint validator
├── tool_approval.py            # HITL approval manager & agent loop recursion guard
├── linked_list.py              # Singly linked list in Python (LC 206, 141, 21, 19)
├── README.md
└── DSA/
    └── LinkedListOperations.java # Singly linked list in Java (LC 206, LC 141, LC 21)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python input_guardrail.py
python pii_detector.py
python output_guardrail.py
python tool_approval.py
python linked_list.py
```

### Java Tests
```bash
cd DSA
javac LinkedListOperations.java
java LinkedListOperations
```

---

## ✅ Status: Completed
