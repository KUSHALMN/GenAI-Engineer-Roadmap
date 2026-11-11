# 🎯 Technical Interview Questions — Day 28: Eval Reporting & Matrix Monotonic Stack

## Question 1: What makes an evaluation dashboard executive-ready and actionable for engineering leadership?
**Answer:**
1. **Delta-Centric Summaries:** Avoid raw numbers; highlight $\Delta$ compared to production baseline and target thresholds (e.g. $+3.3\%$ Faithfulness, $-150\text{ms}$ P95 latency).
2. **Confidence Intervals:** Present bootstrap or Bayesian confidence bounds ($95\%\text{ CI}$) to distinguish statistical noise from genuine regressions.
3. **Failure Slice Breakdowns:** Group regressions by customer cohort, topic taxonomy, or language so domain owners can act immediately.
4. **Actionable Gate Recommendations:** Clear PASS / WARN / BLOCK badges that directly correlate with CI/CD deployment pipelines.

---

## Question 2: In LeetCode 85 (Maximal Rectangle), how do you reduce a 2D matrix problem to repeated 1D histogram calculations?
**Answer:**
- Maintain an array `heights[cols]` representing consecutive 1s in each column up to the current row.
- For each row:
  - If `matrix[row][col] == '1'`, increment `heights[col]++`.
  - If `matrix[row][col] == '0'`, reset `heights[col] = 0` because any rectangle must be contiguous vertically.
- Then treat the current row's heights as a histogram and apply LeetCode 84's monotonic stack algorithm in $O(\text{Cols})$.
- Repeating this for all rows solves the problem in $O(\text{Rows} \times \text{Cols})$ total time and $O(\text{Cols})$ space.
