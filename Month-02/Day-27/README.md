# 📅 Day 27 — Month 02: Guardrails & Safe AI Execution

> Build an end-to-end safety guardrail system for production GenAI architectures: Pre-LLM Input Screening, Post-LLM Output Schema Validation, Confidential PII Detectors with Severity Scoring, and Role-Based Tool Permission Gates with Human-in-the-Loop (HITL). Master Advanced Binary Tree algorithms (LC 543, 124, 297) in Java.

---

## 📁 Architecture Overview

```
Day-27/
├── guardrails/
│   ├── input_guardrail.py    # Pre-execution policy & topic validator
│   ├── output_guardrail.py   # Post-execution safety & confidential disclosure filter
│   ├── schema_validator.py   # Deterministic JSON type & key constraint enforcer
│   ├── pii_detector.py       # Regex & severity-scored PII scanner
│   └── tool_permission.py    # Read/Write/High-Risk role permission matrix
├── examples/
│   └── guardrail_tests.json  # Comprehensive safety test cases
├── DSA/
│   └── BinaryTreeAdvanced.java # LC 543 + LC 124 + LC 297 (Java)
├── Interview/
│   └── technical_questions.md # Guardrail architecture & algorithm Q&A
├── Notes/
│   └── notes.md             # Theoretical deep-dive
└── README.md
```

---

## 🚀 Execution & Verification

### 1. Test Input Guardrail (Python)
```bash
python -c "from guardrails.input_guardrail import InputGuardrail; g = InputGuardrail(); print(g.process('What is LoRA?'))"
```

### 2. Compile & Run Java Tree Suite
```bash
cd Month-02/Day-27/DSA
javac BinaryTreeAdvanced.java && java DSA.BinaryTreeAdvanced
```
