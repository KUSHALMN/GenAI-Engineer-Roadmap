# Day 12: Technical Interview Preparation — Model Evaluation & Two Heaps

### Q1: Why is Perplexity (PPL) alone insufficient for evaluating a fine-tuned instruction model?
**Answer:**
Perplexity measures how well the model predicts words in a test corpus. A model with low perplexity can still generate harmful, non-compliant, or formatted hallucinated outputs. Evaluation must incorporate task-specific downstream metrics: Exact Match (EM), JSON Schema adherence, and domain unit tests.

### Q2: Why is the two-heap pattern optimal for streaming median computation?
**Answer:**
Maintaining a sorted array takes $O(n)$ insertion time. The two-heap approach keeps the smaller half in a max-heap and larger half in a min-heap. Inserting takes $O(\log n)$, and the median is always at the root of one or both heaps ($O(1)$ access).
