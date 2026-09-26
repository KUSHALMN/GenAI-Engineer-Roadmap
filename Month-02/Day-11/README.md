# 📅 Day 41 — Month 02, Day 11: Agent Architecture

> Build a deterministic sequential workflow, an intent router, a tool-using ReAct-style agent loop with failure handling, agent state management, and an architectural analysis of DAG workflows vs autonomous agents. Implement BST operations in Python and Java.

---

## 📁 Structure

```
Day-11/
├── agent_state.py          # State tracking, scratchpad formatting, and checkpointing
├── workflow.py             # Deterministic sequential workflow pipeline
├── router.py               # Intent classifier delegating to Workflow, RAG, or Agent
├── agent_loop.py           # ReAct autonomous tool-calling loop (Reason + Act)
├── agent_vs_workflow.md    # Tradeoffs between deterministic pipelines and autonomous agents
├── bst.py                  # BST search, insert, delete, validate, LCA (LC 700, 701, 450, 98, 235)
├── README.md
└── DSA/
    └── BinarySearchTree.java # BST operations in Java (LC 700, 701, 450, 98, 235)
```

---

## 🧪 Quick Run & Verification

### Python Tests
```bash
python agent_state.py
python workflow.py
python router.py
python agent_loop.py
python bst.py
```

### Java Tests
```bash
cd DSA
javac BinarySearchTree.java
java BinarySearchTree
```

---

## ✅ Status: Completed
