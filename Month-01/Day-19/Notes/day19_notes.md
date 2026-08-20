# Day 19 Study Notes — LLM Tool Calling & Heap (Top-K) Patterns

---

## 🧠 Part 1: Generative AI & Agentic Systems — Tool Calling

### 1. What is Tool Calling / Function Calling?
Large Language Models (LLMs) are text prediction engines with static knowledge cutoff dates and no inherent capability to execute code, perform accurate multi-step arithmetic, or query live APIs. **Tool Calling** bridges the model to the external world.

### 2. The Tool-Calling Lifecycle Loop
```
User Prompt ──> [ LLM (with Tools Schema) ]
                       │
                       ├─► No tool needed ──> Final Response to User
                       │
                       └─► Emits `tool_calls` JSON (name, args)
                                  │
                                  ▼
                         [ Tool Execution ]
                                  │
                                  ▼
                         [ Tool Result Message ]
                                  │
                                  ▼
                    [ LLM (Context + Tool Result) ] ──> Final Response
```

### 3. Key Schema Components
- `tools`: Array of objects defining `type: "function"` and `function: {name, description, parameters}`.
- `parameters`: Formatted as standard JSON Schema (`type: "object"`, `properties: {...}`, `required: [...]`).
- `ChatMessage`: Role transitions:
  - `user`: Initiates prompt.
  - `assistant`: Emits text or `tool_calls: [{id, type, function: {name, arguments}}]`.
  - `tool`: Contains `tool_call_id`, `name`, and `content` (serialized output string).

### 4. Safe Tool Execution Principles
- **Never use `eval()`** for mathematical evaluation; use Python's Abstract Syntax Tree (`ast.parse`) with restricted operators and functions.
- **Always sandbox** external code execution and filesystem modifications.
- **Implement max iterations** to prevent infinite agent loop execution.

---

## ⚡ Part 2: Data Structures & Algorithms — Heaps & Top-K Problems

### 1. Heap Properties & PriorityQueue
- **Binary Heap:** Complete binary tree satisfying the heap invariant.
  - **Min-Heap:** Root element is always the minimum ($parent \le child$).
  - **Max-Heap:** Root element is always the maximum ($parent \ge child$).
- **Complexity:**
  - Insert (`offer` / `push`): $O(\log N)$
  - Extract Root (`poll` / `pop`): $O(\log N)$
  - Peek Root (`peek`): $O(1)$
  - Heapify array: $O(N)$

### 2. Top-K Patterns & Strategies

#### Pattern 1: Min-Heap for Top-K Largest Elements
- Maintain a Min-Heap capped at size $K$.
- Insert each element; if `heap.size() > k`, evict the smallest (`heap.poll()`).
- At termination, the heap holds the $K$ largest elements, and root is the $K$-th largest.
- Time: $O(N \log K)$, Space: $O(K)$.

#### Pattern 2: QuickSelect (Hoare's Selection)
- Partitions the array around a random pivot like QuickSort.
- Rather than recursing into both sides, recurses only into the partition containing the target index.
- Average Time: $O(N)$, Worst-case: $O(N^2)$ (rare with random pivot), In-place Space: $O(1)$.

#### Pattern 3: Bucket Sort for Frequencies
- When frequencies are bounded in $[1, N]$, build an array of lists indexed by frequency.
- Gathering top $K$ runs in strictly $O(N)$ linear time.

---

## 📝 Daily Review Checklist
- [x] Built modular Tool Calling Assistant in Python (`app.py`, `llm.py`, `tool_registry.py`, `schemas.py`, tools).
- [x] Implemented safe AST-based calculator and chat history search/storage tools.
- [x] Implemented LeetCode 215 (Kth Largest Element) with Min-Heap & QuickSelect in Java.
- [x] Implemented LeetCode 347 (Top K Frequent Elements) with Heap & Bucket Sort in Java.
- [x] Implemented LeetCode 973 (K Closest Points to Origin) with Max-Heap & QuickSelect in Java.
- [x] Prepared interview questions across Technical, Coding, and Recruiter rounds.
