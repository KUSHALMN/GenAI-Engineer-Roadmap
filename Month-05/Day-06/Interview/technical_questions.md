# Day 06: Technical Interview Preparation — SFT Loss & Java Streams

### Q1: What is Next-Token Prediction Cross-Entropy Loss in Supervised Fine-Tuning?
**Answer:**
At each token position $t$, the model outputs logits over the vocabulary. Softmax produces probability $P(w_t | w_{<t})$. The loss is the negative log-likelihood: $\mathcal{L} = -\sum_{t} \log P(y_t | y_{<t})$. In instruction SFT, loss is masked (set to -100) over user prompt tokens so gradients only update based on target assistant completion tokens.

### Q2: Are Java Streams always faster than standard `for` loops?
**Answer:**
No. Standard for-loops are generally faster or equal for small arrays because they avoid stream pipeline object allocations, lambda call-site overhead, and autoboxing. Streams excel in readability, immutability, and trivial parallelization (`parallelStream()`) on large datasets.
