# 🎯 Technical Interview Questions — Day 17: Pretraining Loops & Rotated Binary Search

## Question 1: Why is Decoupled Weight Decay (AdamW) strictly required for LLM pretraining instead of standard L2 regularization in Adam?
**Answer:**
- In standard SGD, L2 regularization is mathematically equivalent to weight decay.
- However, in Adam, gradients are divided by the square root of the second momentum ($v_t$). If L2 regularization $\lambda \theta$ is added directly to the gradient, weights with historically large gradients receive *smaller* weight decay, while weights with small gradients receive *disproportionately large* decay.
- **AdamW Formulation:** AdamW decouples weight decay entirely from gradient momentum updates:
  $$\theta_{t+1} = \theta_t - \eta_t \lambda \theta_t - \frac{\eta_t}{\sqrt{v_t} + \epsilon} m_t$$
  This ensures every parameter decays at a uniform rate proportional to the learning rate $\eta_t$, which is essential for training stability across billions of parameters.

---

## Question 2: In LeetCode 154 (Rotated Sorted Array with Duplicates), why does `nums[mid] == nums[right]` degrade worst-case time complexity to O(N)?
**Answer:**
- When `nums[mid] == nums[right]`, it is impossible to determine whether the pivot point lies in the left half or right half (e.g. `[1, 1, 1, 0, 1]` vs `[1, 0, 1, 1, 1]`).
- The only provably safe operation is to decrement `right--`, eliminating one duplicate element without discarding the true minimum (since `nums[mid]` still preserves that value).
- If all elements in the array are identical (e.g. `[1, 1, 1, 1, 1]`), the algorithm decrements `right` one index at a time, resulting in $N$ iterations ($O(N)$ worst-case time), while retaining $O(\log N)$ average time on non-degenerate inputs.
