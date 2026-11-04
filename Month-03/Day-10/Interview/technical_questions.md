# Interview Questions: Query Rewriting & Task Scheduling

### Q1: What is the risk of performing query rewriting with an LLM on every turn?
**Answer**:
1. **Latency Overhead**: Calling an LLM for query rewriting adds 200–800ms before search even begins.
2. **Hallucination Risk**: An LLM rewriter might introduce speculative details not present in the user query.
3. **Cost**: Multiplies token costs.
*Mitigation*: Use fast rule-based heuristics or lightweight SLMs (e.g., fine-tuned 1B/3B models) with strict temperature=0.0.

### Q2: In LC 621 (Task Scheduler), how is the formula for minimum intervals derived?
**Answer**:
Let $M$ be the maximum frequency of any task and $C$ be the number of tasks sharing this maximum frequency.
These tasks create $(M - 1)$ chunks separated by cooldown slots of length $n$.
Each chunk requires space for $(n - (C - 1))$ other tasks.
If there are not enough tasks to fill these idle slots, total time is $(M - 1) \times (n + 1) + C$.
If available tasks exceed idle capacity, the processor never idles, and the answer is simply the total number of tasks `tasks.length`. Thus:
$$\text{Total} = \max(\text{tasks.length}, (M - 1) \times (n + 1) + C)$$

### Q3: Why is a max-heap greedy strategy optimal for LeetCode 767 (Reorganize String)?
**Answer**:
By always picking the two characters with the highest remaining frequencies, we prevent the highest-frequency character from getting "backed into a corner" where it is the only remaining character with adjacent duplicate conflicts.
