# Month 1 - Day 19

## Topics Learned
- LLM Function Calling & Tool Calling API Specs
- Automatic JSON Schema Generation via Python Type Reflection
- Dynamic Tool Registry & Safe Dispatching
- ReAct & Iterative Tool Execution Loops in Agents
- Abstract Syntax Tree (AST) Safe Mathematical Parsing
- Episodic Conversation Memory & Context Lookup
- DSA: Heap (PriorityQueue) Operations & Invariants
- Top-K Problem Patterns (Min-Heap, Max-Heap, QuickSelect, Bucket Sort)

## AI Project
**Tool-Calling AI Assistant (`Month-01/Day-19/AI/tool-calling-assistant/`)**
- Modular assistant supporting OpenAI and Groq function-calling conventions.
- AST-based safe calculator tool (`calculate`).
- Episodic memory tools (`get_chat_history`, `search_chat_history`, `save_chat_summary`).
- Built-in simulation fallback mode when running without API keys.

## DSA (Java)
- **Kth Largest Element in an Array** (`kth_largest.java`): Min-Heap $O(N \log K)$ and QuickSelect $O(N)$ approaches.
- **Top K Frequent Elements** (`top_k_frequent.java`): Min-Heap $O(N \log K)$ and Bucket Sort $O(N)$ linear time approaches.
- **K Closest Points to Origin** (`k_closest_points.java`): Max-Heap with custom Euclidean distance comparator $O(N \log K)$ and QuickSelect $O(N)$.

## Interview Preparation
- **Technical Questions (`Interview/technical_questions.md`)**: LLM function calling internals, JSON mode vs tools, structured outputs, prompt injection defenses, and parallel tool dispatching.
- **Coding Questions (`Interview/coding_questions.md`)**: Heap vs QuickSelect trade-offs, streaming memory constraints, Java `PriorityQueue` comparator nuances, and bucket sort optimizations.
- **Recruiter Questions (`Interview/recruiter_questions.md`)**: STAR-format agent project narratives, API cost/latency optimization, prompt caching, and error resilience.

---

## Folder Structure

```
Day-19/
│
├── AI/
│   └── tool-calling-assistant/
│       ├── app.py
│       ├── llm.py
│       ├── tool_registry.py
│       ├── schemas.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── calculator.py
│       │   └── chat_history.py
│       ├── requirements.txt
│       └── README.md
│
├── DSA/
│   ├── kth_largest.java
│   ├── top_k_frequent.java
│   └── k_closest_points.java
│
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_questions.md
│
├── Notes/
│   └── day19_notes.md
│
├── Resources.md
└── README.md
```

---

## How to Run

### AI Tool-Calling Assistant:
```bash
cd Month-01/Day-19/AI/tool-calling-assistant
pip install -r requirements.txt

# Run automated demo:
python app.py --demo

# Run interactive assistant:
python app.py
```

### DSA (Java):
```bash
cd Month-01/Day-19/DSA

# 1. Kth Largest Element
javac kth_largest.java
java kth_largest

# 2. Top K Frequent Elements
javac top_k_frequent.java
java top_k_frequent

# 3. K Closest Points to Origin
javac k_closest_points.java
java k_closest_points
```
