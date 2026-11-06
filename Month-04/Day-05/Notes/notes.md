# Day 05 Notes: Planner-Executor Pattern

## 1. Architecture Flow
1. **Planner:** Decomposes a macro objective into an actionable DAG of steps.
2. **Executor:** Dispatches tools sequentially or concurrently according to dependencies.
3. **Replanner:** Triggered when a step encounters a tool failure, updating downstream steps.
