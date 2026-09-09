# Day 32 Notes — Month 02, Day 01
## Topic: LLM Fine-Tuning + LoRA + DP (Coin Change)

---

## AI: LLM Fine-Tuning

### Key Concepts
- **Full Fine-Tuning**: All weights updated. High memory cost. Best for large domain shifts.
- **LoRA**: Freeze base model, train low-rank adapters `ΔW = BA`. ~0.06% trainable params.
- **QLoRA**: LoRA on 4-bit quantized base model. Enables 7B fine-tuning on 12GB VRAM.
- **Instruction Tuning**: Fine-tune on `(instruction, input, output)` triples to follow user commands.

### LoRA Hyperparameters
| Param | Typical Value | Effect |
|-------|--------------|--------|
| `r` (rank) | 8–64 | Higher = more capacity, more params |
| `alpha` | 16–64 | Scaling factor; often set to 2×r |
| `dropout` | 0.05 | Regularization on adapter layers |
| `target_modules` | q_proj, v_proj | Which attention projections to adapt |

### Fine-Tuning Pipeline
```
Raw Data → prepare_dataset.py → dataset.jsonl
         → train.py (LoRA) → checkpoint/
         → evaluate.py → BLEU, F1, Exact Match
```

### Evaluation Hierarchy
1. **Perplexity** — training signal only
2. **BLEU / ROUGE** — fast n-gram overlap
3. **BERTScore** — semantic similarity
4. **LLM-as-Judge** — human-aligned quality score

---

## DSA: Coin Change (LC 322) — Dynamic Programming

### Pattern: Unbounded Knapsack DP
```
dp[0] = 0
dp[i] = min(dp[i - coin] + 1) for coin in coins if coin <= i
```

### Complexity
- Time: O(amount × |coins|)
- Space: O(amount)

### Key Insight
- Greedy fails on non-canonical coin systems
- Forward DP (not backward) enables unbounded reuse of each coin
- Reconstruct path using `parent[]` array

---

## Connections
- LoRA's low-rank hypothesis mirrors how DP reduces exponential search to polynomial by exploiting overlapping subproblems — both find minimal representations of complex spaces.
