# 🎯 Technical Interview Questions — Day 10: Triton Custom Kernels & Rabin-Karp

## Question 1: How does OpenAI Triton enable Python developers to write GPU kernels matching CUDA C++ performance without managing thread-level synchronization?
**Answer:**
1. **Block-Level Abstraction:** CUDA requires manual coordinate calculation across threads (`threadIdx.x`, `blockDim.x`), warp synchronization (`__syncwarp()`), and shared memory bank conflict management. Triton operates at the **Block (Tile) level** using `tl.program_id(axis)` and block pointers (`tl.load(ptr + offsets, mask=mask)`).
2. **Compiler Optimization Passes:** The Triton compiler (built on LLVM/MLIR) automatically performs:
   - Coalesced global memory access layout transformations.
   - Vectorization across SIMD registers.
   - Automatic double-buffering and software pipelining between global HBM and shared memory registers.
3. **Operator Fusion:** Multiple consecutive pointwise or reduction steps (e.g. Bias Add + LayerNorm + GeLU) execute within GPU registers in a single kernel invocation, eliminating expensive intermediate round-trips to HBM.

---

## Question 2: In the Rabin-Karp Algorithm, explain how rolling hash recalculates the window hash in O(1) time without re-scanning characters.
**Answer:**
- A string of length $L$ has polynomial hash $H = \sum_{i=0}^{L-1} c_i \cdot B^{L-1-i}$.
- When the window slides one character to the right:
  1. **Subtract Old Character:** Subtract $c_{\text{old}} \cdot B^{L-1}$ to remove the highest-order contribution of the exiting left character.
  2. **Shift Base:** Multiply the remaining hash by base $B$ (shifting each character's exponent up by 1).
  3. **Add New Character:** Add $c_{\text{new}} \cdot B^0$.
- Because each transition uses basic arithmetic ($O(1)$ scalar operations), sliding the window across an $N$-character string runs in strictly $O(N)$ linear time.
