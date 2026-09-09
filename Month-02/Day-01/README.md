# 📅 Day 32 — Month 02, Day 01: LLM Fine-Tuning + LoRA + Coin Change DP

> **Month 02 begins!** Today covers production LLM fine-tuning with LoRA/PEFT, building a full dataset → train → evaluate pipeline in Python, and mastering Dynamic Programming with LeetCode 322 (Coin Change) in Java.

---

## 📁 Structure

```
Day-01/
├── fine_tuning/
│   ├── config.py           # FineTuneConfig dataclass (LoRA hyperparams)
│   ├── prepare_dataset.py  # Format & split raw samples into train/val JSONL
│   ├── train.py            # LoRA fine-tuning loop (stub → swap in HF Trainer)
│   └── dataset.jsonl       # Training samples (instruction-following format)
│
├── evaluation/
│   ├── evaluate.py         # BLEU-1, Keyword F1, Exact Match metrics
│   └── test_samples.jsonl  # Validation samples with expected outputs
│
├── DSA/
│   └── CoinChange.java     # LC 322: Coin Change — Bottom-up DP (Java)
│
├── Interview/
│   ├── technical_questions.md  # LoRA math, PEFT vs full FT, catastrophic forgetting
│   └── coding_questions.md     # Coin Change DP recurrence, greedy failure, path reconstruction
│
├── Notes/
│   └── notes.md            # Key concepts, LoRA hyperparams, DP patterns
└── Resources.md
```

---

## 🧠 AI: LLM Fine-Tuning Pipeline

### Run Dataset Preparation
```bash
cd Month-02/Day-01
python fine_tuning/prepare_dataset.py
```

### Run Training (Simulated LoRA Loop)
```bash
python fine_tuning/train.py
```

### Run Evaluation
```bash
python evaluation/evaluate.py
```

### Key Concepts
| Concept | Detail |
|---------|--------|
| LoRA rank `r` | 16 — controls adapter capacity |
| Alpha | 32 — scaling = alpha/r = 2.0 |
| Trainable params | ~0.06% of base model |
| Dataset format | Alpaca-style instruction tuning |
| Evaluation | BLEU-1, Keyword F1, Exact Match |

---

## ☕ DSA: Coin Change — LC 322 (Java)

**Pattern**: Dynamic Programming — Unbounded Knapsack

```
dp[0] = 0
dp[i] = min(dp[i - coin] + 1)  for each coin ≤ i
```

| Metric | Value |
|--------|-------|
| Time | O(amount × \|coins\|) |
| Space | O(amount) |
| Difficulty | Medium |

### Run
```bash
cd Month-02/Day-01/DSA
javac CoinChange.java
java CoinChange
```

**Expected output:**
```
2
3
-1
0
```

---

## 🎯 Key Takeaways

1. **LoRA** freezes base weights and trains only `BA` adapters — 10-100x memory savings vs full fine-tuning.
2. **Greedy fails** on non-canonical coin systems; DP guarantees optimal via overlapping subproblems.
3. **Evaluation** needs multiple metrics — perplexity alone is insufficient for production LLM quality.
4. **Catastrophic forgetting** is mitigated by PEFT (frozen base), low LR, and data mixing.

---

## ✅ Status: Done
