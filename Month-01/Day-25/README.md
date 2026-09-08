# 📅 Day 25: 📦 Structured Outputs + Pydantic & Trapping Rain Water DSA

Welcome to **Day 25** of the **GenAI Engineer Roadmap**! Today focuses on turning non-deterministic LLM completions into strictly validated, type-safe JSON APIs using Pydantic V2, automated JSON repair heuristics, error feedback self-healing, and mastering LeetCode 42 (Trapping Rain Water) in Java.

---

## 📁 Day 25 Project Structure

```
Day-25/
├── AI/
│   └── structured-outputs/
│       ├── src/
│       │   ├── schemas.py          # Pydantic V2 models with cross-field validators
│       │   ├── validator.py        # Markdown fence stripping & JSON auto-repair
│       │   └── app.py              # FastAPI extraction endpoints (/extract/invoice, /extract/ticket)
│       ├── tests/
│       │   └── test_structured.py # Schema validation & malformed recovery tests
│       ├── requirements.txt
│       └── README.md
│
├── src/
│   ├── schemas.py
│   ├── validator.py
│   └── app.py
├── tests/
│   └── test_structured.py
│
├── DSA/
│   └── trapping_rain_water.java    # LeetCode 42: Trapping Rain Water (Two Pointers & Monotonic Stack)
│
├── Interview/
│   ├── technical_questions.md       # Constrained decoding vs post-generation validation
│   ├── coding_questions.md          # Two-pointer invariant & stack geometry
│   └── recruiter_questions.md       # Self-healing schemas & production resilience
│
├── Notes/
│   └── day25_notes.md
├── Resources.md
└── README.md
```

---

## ⚡ Core Concepts Learned

1. **Pydantic V2 Validation**: Deep type checking, regex constraints, and cross-field consistency.
2. **Defensive JSON Repair**: Rescuing outputs with markdown code blocks, unescaped quotes, or trailing commas.
3. **Self-Healing LLM Retry Loop**: Translating validation errors into actionable retry prompts.
4. **Trapping Rain Water DSA**: Optimal $O(n)$ time, $O(1)$ space two-pointer traversal.

---

## 🚀 Execution Commands

### Test Python Structured Outputs
```bash
python -m pytest Month-01/Day-25/tests/test_structured.py -v
```

### Run Trapping Rain Water Java Solution
```bash
javac Month-01/Day-25/DSA/trapping_rain_water.java
java -cp Month-01/Day-25/DSA trapping_rain_water
```
