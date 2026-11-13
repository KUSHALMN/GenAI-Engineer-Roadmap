# 📝 Notes — Day 14: Numerical Stability & Monotonic Stack

- **Gradient Clipping by Norm:** $g = g \times \min(1.0, \frac{\text{max\_norm}}{\|g\|_2 + 10^{-6}})$ protects the pretraining run from catastrophic loss spikes caused by bad data batches.
- **Histogram Width Formula:** When popping height $h$, the right boundary is $i - 1$ and the left boundary is `stack.peek() + 1`. Width = $(i - 1) - (\text{stack.peek()} + 1) + 1 = i - \text{stack.peek()} - 1$.
