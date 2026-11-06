# Day 04: Technical Interview Preparation — ReAct Agent Loops

### Q1: What causes infinite loops in ReAct agents and how do you mitigate them?
**Answer:**
Causes:
1. Model fails to realize the observation has answered the question and keeps querying the same tool.
2. Tool repeatedly returns an error or empty result, and the agent repeats the exact same arguments.
Mitigations:
- **Hard Max Step Cap:** Break the loop after $N$ turns (e.g., 5 to 10).
- **Repetition Detection:** Hash `(action, action_input)` pairs; if the same call occurs twice consecutively, append a system warning to the scratchpad forcing replanning.
- **Budget Enforcers:** Enforce wall-clock and token consumption limits.

### Q2: Why does Combination Sum allow element reuse by passing index `i` instead of `i + 1`?
**Answer:**
In standard combinations or subsets, each element is used at most once, so we advance to `i + 1`. In unbounded knapsack or Combination Sum where an element can be selected repeatedly, remaining at index `i` permits the recursive step to pick `candidates[i]` again until the target remaining is reduced or pruned.
