# 📝 Notes — Day 17: Pretraining Loops & Binary Search

- **Cosine Warmup Rationale:** Linear warmup from 0 prevents large random weight updates during the unstable initial iterations when Adam's running second moment $v_t$ is uncalibrated.
- **Binary Search Integer Overflow:** Always compute `mid` using `left + (right - left) / 2` to prevent 32-bit signed integer overflow.
