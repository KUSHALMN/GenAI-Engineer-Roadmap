# Day 02 Notes: Instruction Dataset Design

## 1. High-Quality Dataset Principles
1. **Diversity Over Volume:** 1,000 diverse, manually verified samples frequently outperform 50,000 repetitive synthetic rows (LIMA paper).
2. **Strict Role Alternation:** `system -> user -> assistant -> user -> assistant`.
3. **No Target Leaks:** Ensure assistant responses never end abruptly or carry template markers.
