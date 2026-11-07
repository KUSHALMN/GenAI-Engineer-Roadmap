# Day 08 Notes: LoRA Mechanics

## 1. LoRA Mathematical Formulation
$$W = W_0 + \frac{\alpha}{r}(B \cdot A)$$
- $W_0 \in \mathbb{R}^{d \times k}$ (Frozen)
- $A \in \mathbb{R}^{r \times k}$ (Gaussian initialization)
- $B \in \mathbb{R}^{d \times r}$ (Zero initialization)
- Scaling factor: $\alpha / r$ stabilizes gradients across different rank values.
