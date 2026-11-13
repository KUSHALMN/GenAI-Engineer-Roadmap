# 🎯 Technical Interview Questions — Day 14: Mixed Precision & Monotonic Stack

## Question 1: Why did BF16 completely replace FP16 in modern LLM pretraining, and how do FP8 E4M3 and E5M2 differ?
**Answer:**
1. **BF16 vs FP16 Dynamic Range:**
   - **FP16:** 5 exponent bits, 10 mantissa bits. Maximum representable value is 65,504. Gradients in large Transformers routinely exceed this or underflow below $10^{-5}$, requiring fragile dynamic loss scaling.
   - **BF16:** 8 exponent bits (identical to FP32), 7 mantissa bits. Maximum value is $\sim 3.4 \times 10^{38}$. BF16 matches FP32's dynamic range, eliminating gradient overflow and underflow without loss scaling.
2. **FP8 Formats (NVIDIA Hopper / H100):**
   - **E4M3 (1 sign, 4 exponent, 3 mantissa):** Higher precision ($2^{-3} = 0.125$), smaller range (max 448). Used for forward activations and weights where numeric precision is critical.
   - **E5M2 (1 sign, 5 exponent, 2 mantissa):** Matches FP16 dynamic range (max 57,344), lower precision. Used for backward gradient propagation where preserving dynamic range is paramount.

---

## Question 2: In LeetCode 84, prove that each bar index is pushed and popped at most once, and why adding a 0-height sentinel at index N guarantees correctness.
**Answer:**
- **Strictly Monotonic Stack:** The stack stores indices of bars with monotonically non-decreasing heights.
- **Single Push and Pop:** A bar is pushed when it is $\ge$ the current top. When a strictly shorter bar arrives, elements taller than it are popped and their maximal width is computed. Because an index is pushed once and popped at most once, total runtime across $N$ elements is strictly bounded by $2N$ operations ($O(N)$ linear time).
- **Sentinel at index N:** If the array is strictly increasing (e.g. `[1, 2, 3]`), no elements would ever be popped during the initial loop. Appending a virtual bar of height 0 at index $N$ is strictly smaller than any positive height, guaranteeing that all remaining bars are cleanly flushed and calculated before the function returns.
