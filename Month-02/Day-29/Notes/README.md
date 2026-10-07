# 📅 Day 29 — Month 02: Autonomous Agents & State Machine Workflows

> Build an end-to-end Autonomous Agent framework: ReAct (Reasoning + Acting) Execution Loop, State Schema with Scratchpads & Step Budgets, Dynamic Semantic Tool Selection, Intent Routing, and Deterministic Workflow Pipelines. Master Advanced Heaps and Priority Queues (LC 23, 347, 295) in Java.

---

## 📁 Architecture Overview

```
Day-29/
├── AI/
│   ├── agents/
│   │   ├── agent_loop.py         # ReAct autonomous reasoning engine
│   │   ├── state.py              # Agent state schema & status transitions
│   │   ├── tool_selection.py     # Semantic relevance tool filter
│   │   ├── router.py             # Intent classification router
│   │   └── workflow.py           # Deterministic sequential workflow DAG
│   └── examples/
│       └── agent_trace.json      # Multi-step execution audit trace
├── Java/
│   └── HeapAdvancedPatterns.java # LC 23 + LC 347 + LC 295 (Java)
├── DSA/
│   └── HeapAdvancedPatterns.java # Alternate DSA reference
├── Interview/
│   └── technical_questions.md    # Agent architectures & Heap algorithms Q&A
├── Notes/
│   ├── notes.md                  # Theoretical deep-dive
│   └── README.md                 # Day documentation copy
└── README.md
```

---

## 🚀 Execution & Verification

### 1. Test ReAct Autonomous Agent (Python in `AI/`)
```bash
python Month-02/Day-29/AI/agents/agent_loop.py
```

### 2. Compile & Run Java Heap Suite (in `Java/`)
```bash
cd Month-02/Day-29/Java
javac HeapAdvancedPatterns.java && java HeapAdvancedPatterns
```
