# 📅 Day 01 — Month 03: Context Engineering & Multi-Tier Conversation Memory

> Build an enterprise context management and multi-tier memory system: Token Budget Allocators, Sliding Window Conversation Memory, Abstractive Summarizers, Long-term Episodic Memory Stores, and Context Assembly Pipelines. Master Disjoint Set Union (DSU) and Kruskal's Minimum Spanning Tree (LC 547, 684, 1584) in Java.

---

## 📁 Architecture Overview

```
Day-01/
├── AI/
│   ├── memory/
│   │   ├── conversation_memory.py # Sliding window buffer history
│   │   ├── token_budget.py        # Context window token partition manager
│   │   ├── summarizer.py          # Progressive narrative compressor
│   │   ├── memory_store.py        # Persistent user traits & episodic store
│   │   └── memory_retrieval.py    # Semantic relevance search over past memories
│   └── context/
│       └── context_manager.py     # End-to-end prompt context assembler
├── DSA/
│   └── DisjointSetMST.java        # Alternate DSA reference
├── Interview/
│   └── technical_questions.md     # Context engineering & graph DSU Q&A
├── Notes/
│   ├── notes.md                   # Theoretical deep-dive
│   └── README.md                  # Day documentation copy
└── README.md
```

---

## 🚀 Execution & Verification

### 1. Test Context Manager & Memory Pipeline (Python in `AI/`)
```bash
python Month-03/Day-01/AI/context/context_manager.py
```

### 2. Compile & Run Java DSU Suite (in `Java/`)
```bash
cd Month-03/Day-01/DSA
javac DisjointSetMST.java && java DisjointSetMST
```
