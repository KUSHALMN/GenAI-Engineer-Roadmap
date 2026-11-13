# 📝 Notes — Day 11: MoE Expert Routing & Edit Distance

- **Capacity Factor (CF):** Maximum tokens an expert can accept is $\text{Capacity} = \lceil \frac{N \times K}{E} \times CF \rceil$. Excess tokens exceeding this ceiling are dropped (passed through residual without FFN) to prevent GPU stragglers during all-to-all dispatch.
- **Top-2 Weight Normalization:** When using Top-2 gating, always renormalize weights so $w_1 + w_2 = 1.0$ before combining expert outputs.
- **Edit Distance Recurrence:** $\text{dp}[i][j] = 1 + \min(\text{replace}, \min(\text{insert}, \text{delete}))$.
