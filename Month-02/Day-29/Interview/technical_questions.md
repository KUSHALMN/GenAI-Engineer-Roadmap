# 🎯 Day 29 Technical Interview Questions & Answers

## 1. What is the fundamental difference between an Autonomous ReAct Agent and a Deterministic Workflow DAG (e.g. LangGraph vs linear chains)?
**Answer:**
- **Autonomous ReAct Agent (Reasoning + Action Loop)**: The execution path is not hardcoded. At each step, the LLM observes the environment, reasons about what is missing, chooses a tool from a dynamic registry, and loops until it decides it has gathered sufficient context to generate the final answer. Advantage: High adaptability to unforeseen problem variants. Disadvantage: Higher latency, non-deterministic cost, risk of infinite loops.
- **Workflow DAG (State Graph)**: Defines explicit conditional edges, routing nodes, and transitions between discrete states. The path taken is constrained by deterministic code predicates. Advantage: Highly reliable, predictable latency, lower error rates.
- **Production Standard**: Hybrid architectures where high-level state transitions are governed by a deterministic DAG/Router, and isolated leaf tasks are delegated to bounded autonomous agents.

---

## 2. How do you prevent Infinite Loops and Execution Drift in Agentic Workflows?
**Answer:**
1. **Hard Step Limits**: Configure a strict `max_steps` threshold (e.g., 5-8 iterations). If exceeded, forcibly transition to a graceful failure or ask the user for clarification.
2. **Action / Scratchpad Deduplication**: Track historical tool calls in `tool_history`. If the agent calls the identical tool with identical arguments consecutively, intervene with a prompt injection correcting the loop.
3. **Budget Caps**: Terminate the loop if token consumption or elapsed execution time crosses an upper dollar threshold.
4. **Intermediate State Checkpointing**: Persist state to Postgres or Redis after each action to support resumption or rollbacks.

---

## 3. How does the Dual-Heap design in LeetCode 295 provide $O(\log N)$ insertion and $O(1)$ median retrieval?
**Answer:**
A continuous sorted array requires $O(N)$ shift operations per insertion.
The Dual-Heap approach partitions the continuous stream into two halves:
- `lowerMaxHeap`: stores the smaller $50\%$ of numbers; its peek is the largest among the smaller half.
- `upperMinHeap`: stores the larger $50\%$ of numbers; its peek is the smallest among the larger half.
Invariants maintained during insertion:
1. Every element in `lowerMaxHeap` $\le$ every element in `upperMinHeap`.
2. The sizes of both heaps differ by at most 1 ($|\text{size}_1 - \text{size}_2| \le 1$).
Therefore, the median is either the peek of the larger heap (odd total elements) or the average of both heap peeks (even total elements), computed in $O(1)$ time. Insertion takes $O(\log N)$ heap push/pop operations.
