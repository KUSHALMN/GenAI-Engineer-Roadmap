# Technical Interview Preparation — Multimodal Safety & 1D DP
1. Visual Prompt Injections: Malicious instructions printed in faint light-gray text on white backgrounds or tiny 1px fonts. Defenses include OCR pre-filtering, contrast enhancement, and boundary isolation.
2. Space Optimization in 1D DP: When $dp[i]$ depends only on $dp[i-1]$ and $dp[i-2]$, rolling variables reduce space from $O(N)$ to $O(1)$.
