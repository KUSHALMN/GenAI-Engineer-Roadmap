# Day 32 (Month 02 - Day 01): Technical Interview Questions
## Focus: LLM Fine-Tuning, LoRA, PEFT, and Evaluation

---

### Q1: What is the difference between full fine-tuning and Parameter-Efficient Fine-Tuning (PEFT)?

**Answer:**
- **Full fine-tuning** updates all model weights. For a 7B parameter model this requires ~28GB VRAM (fp32) or ~14GB (bf16), plus optimizer states (Adam doubles memory). Impractical on consumer hardware.
- **PEFT** freezes the base model and only trains a small set of adapter parameters:
  - **LoRA**: Injects low-rank matrices `A (d×r)` and `B (r×d)` into attention layers. Only `2×d×r` params per layer are trained. With `r=16` on a 7B model, trainable params drop from 7B to ~4M (~0.06%).
  - **Prefix Tuning**: Prepends trainable soft tokens to the key/value sequence.
  - **Adapter Layers**: Inserts small bottleneck FFN modules between transformer layers.
- **Trade-off**: PEFT is 10-100x more memory efficient but may underfit on very large domain shifts where full fine-tuning excels.

---

### Q2: Explain the LoRA math. Why does low-rank decomposition work?

**Answer:**
1. **Original weight update**: `ΔW ∈ R^(d×d)` — full rank update is expensive.
2. **LoRA hypothesis**: The intrinsic rank of weight updates during fine-tuning is low. Aghajanyan et al. (2020) showed pre-trained models have low "intrinsic dimensionality."
3. **Decomposition**: `ΔW = B × A` where `A ∈ R^(r×d)`, `B ∈ R^(d×r)`, rank `r << d`.
4. **Forward pass**: `h = W₀x + (B × A)x × (α/r)` — `α` is a scaling hyperparameter.
5. **Initialization**: `A` is random Gaussian, `B` is zero → `ΔW = 0` at start, preserving base model behavior.
6. **Merge at inference**: `W = W₀ + BA` — zero latency overhead after merging.

---

### Q3: What evaluation metrics matter for fine-tuned LLMs and why is perplexity insufficient alone?

**Answer:**
- **Perplexity**: Measures how well the model predicts the validation set. Low perplexity ≠ high task quality (a model can memorize training data and score low perplexity but hallucinate on new inputs).
- **Task-specific metrics**:
  - **BLEU / ROUGE**: N-gram overlap for summarization/translation. Fast but penalizes valid paraphrases.
  - **BERTScore**: Semantic similarity using contextual embeddings. Better than n-gram for open-ended generation.
  - **Exact Match (EM)**: For QA tasks where the answer is a span.
  - **LLM-as-Judge**: Use a stronger model (GPT-4) to score outputs on criteria like helpfulness, accuracy, and safety. Scales well but introduces model bias.
- **Best practice**: Use a combination — perplexity for training signal, task metric for validation, LLM-as-Judge for final human-aligned evaluation.

---

### Q4: What is catastrophic forgetting and how do you mitigate it during fine-tuning?

**Answer:**
- **Catastrophic forgetting**: When fine-tuning on domain data, the model overwrites general knowledge, degrading performance on tasks it previously handled well.
- **Mitigations**:
  1. **LoRA / PEFT**: Frozen base weights cannot be overwritten; adapters learn delta only.
  2. **Low learning rate**: `2e-5` to `2e-4` with warmup prevents large weight shifts.
  3. **Replay / data mixing**: Mix 5-10% general instruction data into the fine-tuning set.
  4. **Elastic Weight Consolidation (EWC)**: Penalizes changes to weights important for previous tasks (Fisher information matrix).
  5. **Early stopping**: Monitor validation loss on a held-out general benchmark.
