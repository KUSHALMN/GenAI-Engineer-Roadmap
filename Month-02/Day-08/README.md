# 📅 Day 38 — Month 02, Day 08: GenAI Security

> Build prompt-injection test cases, input sanitization/validation, tool permission enforcement with RBAC, output secret filtering, and a threat model for RAG poisoning and data exfiltration. Implement Binary Search patterns in Python and Java.

---

## 📁 Structure

```
Day-08/
├── security_test_cases.jsonl   # Dataset with direct/indirect injection & jailbreaks
├── prompt_injection_tests.py   # Input sanitizer and automated security test suite runner
├── tool_permissions.py         # Role-Based Access Control and path-traversal validator
├── output_validator.py         # Leakage scanner for API keys, canaries, and system prompts
├── threat_model.md             # Threat model covering RAG poisoning & data exfiltration
├── binary_search.py            # Binary search patterns (LC 704, 33, 153, 34)
├── README.md
└── DSA/
    └── BinarySearchPatterns.java # Binary search in Java (LC 704, 33, 153)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python prompt_injection_tests.py
python tool_permissions.py
python output_validator.py
python binary_search.py
```

### Java Tests
```bash
cd DSA
javac BinarySearchPatterns.java
java BinarySearchPatterns
```

---

## ✅ Status: Completed
