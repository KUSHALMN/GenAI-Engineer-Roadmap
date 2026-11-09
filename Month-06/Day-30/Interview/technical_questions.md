# Technical Interview Preparation — Project Release & Hard Tree Recursion
1. Production Readiness Review: Multi-modal SLAs (TTFT < 50ms, TTFA < 300ms), 99.9% uptime, zero plaintext secrets, automated regression suites.
2. Binary Tree Maximum Path Sum: Return single-branch max gain to parent `node.val + max(leftGain, rightGain)` while updating global path sum `node.val + leftGain + rightGain`.
