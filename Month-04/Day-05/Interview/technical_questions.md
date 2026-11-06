# Day 05: Technical Interview Preparation — Planner-Executor Architecture

### Q1: Compare Planner-Executor with ReAct in terms of token usage and reliability.
**Answer:**
- **Planner-Executor:** Generates a structured multi-step plan in one shot. The executor then runs tools without querying the LLM between every step unless replanning is triggered. Saves tokens and reduces latency on predictable multi-step tasks.
- **ReAct:** Queries the LLM at every single step, incurring an observation prompt accumulation cost. Better for exploratory searches where subsequent steps cannot be predicted upfront.

### Q2: Why is in-place state restoration (e.g. `board[r][c] = '#'`) superior to a `visited` boolean matrix in grid backtracking?
**Answer:**
Allocating a boolean `boolean[][] visited` for each search requires $O(m \cdot n)$ space and allocations. Modifying `board[r][c]` in-place to an impossible character (e.g. `'#'`) and restoring it upon return operates in $O(1)$ auxiliary space and minimizes garbage collector pressure.
