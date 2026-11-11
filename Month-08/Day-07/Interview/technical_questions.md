# 🎯 Technical Interview Questions — Day 07: Regression Gates & Linked Lists

### 1. How do you design an automated regression gate in CI/CD for prompt template modifications?
**Answer:**
1. Maintain an immutable golden evaluation dataset (`N=100` representative queries).
2. On every PR modifying prompts or system cards, run the candidate prompt through the test harness in parallel.
3. Compare candidate scores against the production baseline. If accuracy, faithfulness, or safety drops by $> 2\%$, fail the GitHub Actions job and block merging.

### 2. Why is iterative linked list reversal preferred over recursive reversal in production?
**Answer:**
Iterative reversal runs in $O(1)$ space with three pointer references (`prev`, `curr`, `nextTemp`). Recursive reversal requires $O(N)$ call stack frames, triggering a `StackOverflowError` if the list contains 10,000+ nodes.
