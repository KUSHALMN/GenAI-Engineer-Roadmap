# Day 08: Technical Interview Preparation — LoRA Mechanics & Amortized Analysis

### Q1: In LoRA, why is matrix $B$ initialized to zero while matrix $A$ is initialized with Gaussian noise?
**Answer:**
If both $A$ and $B$ were initialized randomly, $\Delta W = B \cdot A$ would produce a non-zero perturbation at step 0, degrading base model performance immediately. Initializing $B=0$ ensures $\Delta W = 0$ at the start of training, meaning the model begins with its exact original pretrained behavior.

### Q2: Why is the amortized cost of inserting $N$ elements into a dynamic array $O(1)$ when doubling, but $O(N)$ when increasing by a fixed constant $K$?
**Answer:**
- **Doubling ($2\times$):** Copies happen at sizes $1, 2, 4, 8, \dots, N$. The sum of copies is $1 + 2 + 4 + \dots + N = 2N - 1$. Total operations for $N$ inserts $\approx 3N$, so average cost per insert is $3N / N = O(1)$.
- **Fixed Increase ($+K$):** Copies occur $N/K$ times, summing to $K + 2K + 3K + \dots + N = O(N^2)$. Total operations divided by $N$ gives $O(N)$ per insert.
