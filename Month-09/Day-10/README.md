# 📅 Day 10 — Triton Custom Kernels & Rabin-Karp Rolling Hash

## Overview
Simulating OpenAI Triton custom GPU kernel execution and operator fusion (Fused Add + RMSNorm) alongside solving LeetCode 187 (Repeated DNA Sequences) using Rabin-Karp $O(1)$ polynomial rolling hash.

## Components
- `AI/triton_kernel_simulator.py`: Block-level grid scheduling (`program_id`), boundary load masking, and fused operator execution.
- `DSA/RabinKarpRollingHash.java`: $O(1)$ window transition polynomial rolling hash for repeated substring extraction.
- `Interview/technical_questions.md`: Triton compiler architecture vs CUDA C++ and rolling hash mathematical derivation.
- `Notes/notes.md`: GPU boundary protection and hash base selection.
