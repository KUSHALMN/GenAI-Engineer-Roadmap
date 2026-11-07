# Day 11: Technical Interview Preparation — Experiment Tracking & MinStack

### Q1: What key artifacts must be versioned for 100% fine-tuning reproducibility?
**Answer:**
1. Git commit hash of the training repository.
2. Exact dataset snapshot hash / commit.
3. Random seed.
4. Base model checkpoint revision ID.
5. Hyperparameters (learning rate, schedule, batch size, rank, alpha).
6. Environment package manifest (`pip freeze`).

### Q2: How can MinStack be implemented in $O(1)$ extra space without an auxiliary stack?
**Answer:**
By storing the delta $2x - \text{min}$ whenever a new minimum is encountered. If pushed element $x < \text{min}$, push $2x - \text{min}$ and update $\text{min} = x$. During pop, if top value $< \text{min}$, restore previous min via $\text{prevMin} = 2\text{min} - \text{top}$.
