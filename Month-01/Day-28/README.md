# 📅 Day 28: 🔐 GenAI Security & Word Ladder DSA

Welcome to **Day 28** of the **GenAI Engineer Roadmap**! Today focuses on engineering enterprise GenAI security firewalls, mitigating OWASP LLM Top 10 vulnerabilities, detecting prompt injection & delimiter spoofing, implementing canary token leak detection, and mastering LeetCode 127 (Word Ladder) with Bidirectional BFS in Java.

---

## 📁 Day 28 Project Structure

```
Day-28/
├── AI/
│   └── security-firewall/
│       ├── src/
│       │   ├── firewall.py         # Injection scanner, obfuscation decoding, canary leak detector
│       │   └── app.py              # FastAPI security inspection gateway
│       ├── tests/
│       │   └── test_security.py    # Injection tests, canary leak tests, quarantine tests
│       ├── requirements.txt
│       └── README.md
│
├── src/
│   ├── firewall.py
│   └── app.py
├── tests/
│   └── test_security.py
│
├── DSA/
│   └── word_ladder.java            # LeetCode 127: Word Ladder (Optimal Bidirectional BFS)
│
├── Interview/
│   ├── technical_questions.md       # Indirect prompt injection, canary token architecture
│   ├── coding_questions.md          # Bidirectional BFS state pruning
│   └── recruiter_questions.md       # Autonomous agent safety & least-privilege security
│
├── Notes/
│   └── day28_notes.md
├── Resources.md
└── README.md
```

---

## ⚡ Core Concepts Learned

1. **OWASP Top 10 for LLMs**: Defending against direct/indirect prompt injection and system prompt leakage.
2. **Canary Tokens**: Dynamic tripwires preventing confidential prompt exfiltration.
3. **Payload Obfuscation Scanning**: Unpacking Base64 and special delimiter tokens.
4. **Bidirectional BFS**: Shrinking exponential branch complexity to $2 \cdot O(b^{d/2})$ in Java.

---

## 🚀 Execution Commands

### Test Security Firewall Suite
```bash
python -m pytest Month-01/Day-28/tests/test_security.py -v
```

### Run Word Ladder Java Solution
```bash
javac Month-01/Day-28/DSA/word_ladder.java
java -cp Month-01/Day-28/DSA word_ladder
```
