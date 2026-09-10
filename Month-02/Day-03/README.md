# 📅 Day 33 — Month 02, Day 03: LangChain Agents + Tool Use + House Robber DP

> Build a production LangChain tool-calling agent with Search, Calculator, and Weather tools backed by Groq LLaMA3. Master House Robber (LC 198 & 213) DP patterns in Java.

---

## 📁 Structure

```
Day-03/
├── src/
│   ├── main.py         # FastAPI entrypoint — POST /agent/run
│   ├── model.py        # LangChain agent + 3 custom tools (Search, Calc, Weather)
│   ├── inference.py    # Agent runner → structured AgentResponse
│   └── schemas.py      # Pydantic schemas for tool inputs & agent response
│
├── tests/
│   └── test_inference.py   # Unit tests for tools, schemas, calculator logic
│
├── benchmark/
│   └── benchmark.md        # Latency, token usage, tool accuracy analysis
│
├── DSA/
│   └── HouseRobber.java    # LC 198 + LC 213 — 1D DP, O(1) space (Java)
│
├── Interview/
│   ├── technical_questions.md  # ReAct pattern, prompt injection, AgentExecutor vs LangGraph
│   └── coding_questions.md     # House Robber recurrence, circular variant, DP patterns
│
└── requirements.txt
```

---

## 🧠 AI: LangChain Tool-Calling Agent

### Setup
```bash
cd Month-02/Day-03
pip install -r requirements.txt
cp .env.example .env   # add GROQ_API_KEY
```

### Run FastAPI Server
```bash
uvicorn src.main:app --reload
# POST http://localhost:8000/agent/run
# Body: {"query": "What is 15 * 24 + 100?"}
```

### Run Inference Directly
```bash
python src/inference.py
```

### Run Tests
```bash
pytest tests/test_inference.py -v
```

### Tools Available
| Tool | Input | Description |
|------|-------|-------------|
| `calculator_tool` | math expression | Safe AST-based eval |
| `weather_tool` | city, units | Current weather lookup |
| `search_tool` | query, max_results | Web search |

### Agent Flow
```
User Query
    ↓
LLM (LLaMA3-8B via Groq) — selects tool + generates input
    ↓
Tool Execution (calculator / weather / search)
    ↓
LLM synthesizes final answer from tool output
    ↓
AgentResponse (answer, tool_used, steps)
```

---

## ☕ DSA: House Robber — LC 198 + LC 213 (Java)

**Pattern**: 1D Dynamic Programming — skip-adjacent constraint

```
dp[i] = max(dp[i-1], dp[i-2] + nums[i])
```
Space-optimized to O(1) using two variables.

| Problem | Variant | Time | Space |
|---------|---------|------|-------|
| LC 198 | Linear array | O(n) | O(1) |
| LC 213 | Circular array | O(n) | O(1) |

### Run
```bash
cd Month-02/Day-03/DSA
javac HouseRobber.java
java HouseRobber
```

**Expected output:**
```
4
12
5
2
3
4
```

---

## 🎯 Key Takeaways

1. **Native tool calling** (JSON schema) is more reliable than text-based ReAct parsing — no regex fragility.
2. **Safe eval** via `ast.parse` + operator whitelist prevents calculator injection attacks.
3. **House Robber** reduces to two variables — classic O(n) → O(1) space DP optimization.
4. **LC 213 circular** = run linear robber twice on two non-overlapping ranges, take max.

---

## ✅ Status: Done
