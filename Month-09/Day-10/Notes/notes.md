# 📝 Notes — Day 10: Triton Kernels & Rabin-Karp Rolling Hash

- **Triton Boundary Masking:** `tl.load(ptr, mask=offsets < N, other=0.0)` prevents GPU memory segmentation faults on tensor dimensions that are not exact multiples of the block size.
- **Rabin-Karp Base Selection:** For DNA strings (4 alphabet characters), choose $B = 4$. For general ASCII, choose a prime base $B = 31$ or $257$ with prime modulo $10^9 + 7$.
