# Month 1 - Day 20

## 📚 Topics Learned
- Autonomous AI Research Agents & The ReAct (Reasoning + Action) Paradigm
- BM25 Inverted Index Information Retrieval & Corpus Indexing
- Safe Abstract Syntax Tree (AST) Mathematical Evaluation & Security
- Reflection, Self-Correction, and Structured Report Synthesis
- Multi-Provider LLM Tool Calling (Groq / OpenAI / Offline Simulation Mode)
- Graph Representation & Traversal (BFS & DFS on Grids and Graph Adjacency Lists)
- Connected Components & Island Sinking Algorithms
- Deep Memory Graph Serialization & Cycle Isolation (`Map<Node, Node>`)
- Topological Sorting & Directed Acyclic Graph (DAG) Cycle Detection (Kahn's Algorithm & 3-State DFS)

---

## 🤖 AI Project: Autonomous Research Agent (`AI/research-agent/`)
A production-ready autonomous research agent that decomposes complex technical questions, searches seminal AI research papers using BM25 lexical ranking, evaluates mathematical formulas (FLOPs, scaling laws, memory footprint) via a secure AST calculator, and synthesizes structured reports with complete source citations.

---

## 🧩 DSA (Java): Graph Algorithms
1. **Number of Islands** (`number_of_islands.java`): LeetCode 200 - DFS Sink $O(M \times N)$, BFS Queue $O(M \times N)$ with $O(\min(M, N))$ space, and Disjoint Set Union (Union-Find).
2. **Clone Graph** (`clone_graph.java`): LeetCode 133 - Deep copy of cyclic undirected graph using DFS and BFS with `HashMap<Node, Node>` reference isolation.
3. **Course Schedule** (`course_schedule.java`): LeetCode 207 - Cycle detection in directed graphs using Kahn's Algorithm (BFS In-Degree Queue) and 3-State DFS Coloring.

---

## 📝 Interview Preparation
- **Technical Questions (`Interview/technical_questions.md`)**: ReAct vs CoT, preventing infinite agent loops, AST security vs `eval()`, GraphRAG vs Vector RAG, and MoE sparse activation mechanics.
- **Coding Questions (`Interview/coding_questions.md`)**: BFS vs DFS space complexity trade-offs, graph deep copy mechanics, cycle detection algorithms, recursion stack overflow mitigation, and BM25 time complexity.
- **Recruiter Questions (`Interview/recruiter_questions.md`)**: STAR-format responses for deploying autonomous agents, latency/cost optimization on Groq LPU, debugging complex recursion issues, and compound AI architectures.

---

## 📁 Folder Structure

```
Day-20/
│
├── Notes/
│   └── day20_notes.md
│
├── AI/
│   └── research-agent/
│       ├── app.py
│       ├── agent.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── document_search.py
│       │   └── calculator.py
│       ├── schemas.py
│       ├── config.py
│       ├── requirements.txt
│       └── README.md
│
├── DSA/
│   ├── number_of_islands.java
│   ├── clone_graph.java
│   └── course_schedule.java
│
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_questions.md
│
├── Resources.md
└── README.md
```

---

## 🚀 How to Run

### 1. AI Research Agent:
```bash
cd Month-01/Day-20/AI/research-agent
pip install -r requirements.txt

# Run automated benchmark suite:
python app.py --demo

# Run single query with markdown export:
python app.py --query "Analyze DeepSeek-V3 MoE architecture and calculate activated parameter ratio" --export report.md

# Run interactive shell:
python app.py
```

### 2. DSA (Java Solutions & Test Suites):
```bash
cd Month-01/Day-20/DSA

# Number of Islands
javac number_of_islands.java
java number_of_islands

# Clone Graph
javac clone_graph.java
java clone_graph

# Course Schedule
javac course_schedule.java
java course_schedule
```
