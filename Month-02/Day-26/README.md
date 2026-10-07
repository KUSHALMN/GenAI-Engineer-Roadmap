# 📅 Day 26 — Month 02: GenAI Security & Prompt Injection Defense

> Implement a defense-in-depth security harness for LLM applications: Unicode & Zero-Width Sanitization, Token Denial-of-Service Guards, Regex & Pattern-based PII Scrubber, Strict Tool Execution Allowlists, and Multi-vector Prompt Injection Detectors. Master Fast & Slow Pointer algorithms (LC 141, 142, 234) in Java.

---

## 📁 Architecture Overview

```
Day-26/
├── security/
│   ├── prompt_injection.py   # Multi-vector injection & jailbreak detection
│   ├── input_validation.py  # Unicode normalization & control character scrubber
│   ├── pii_filter.py        # Sensitive PII pattern identification & masking
│   ├── tool_allowlist.py    # Strict role-based tool permission execution policy
│   └── token_limit.py       # Context exhaustion & DoS ceiling protector
├── examples/
│   └── malicious_prompts.json # Adversarial threat dataset
├── DSA/
│   └── LinkedListCyclePatterns.java # LC 141 + LC 142 + LC 234 (Java)
├── Interview/
│   └── technical_questions.md # Security architecture & algorithm Q&A
├── Notes/
│   └── notes.md             # Security engineering deep-dive
└── README.md
```

---

## 🚀 Execution & Verification

### 1. Test Injection Detector (Python)
```bash
python Month-02/Day-26/security/prompt_injection.py
```

### 2. Compile & Run Java DSA Suite
```bash
cd Month-02/Day-26/DSA
javac LinkedListCyclePatterns.java && java DSA.LinkedListCyclePatterns
```
