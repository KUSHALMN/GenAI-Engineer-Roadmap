# Day 20: Technical Interview Questions & Deep Dives

---

### Q1: What is the fundamental difference between the ReAct (Reasoning + Action) framework and standard Chain-of-Thought (CoT) prompting? When should you choose one over the other?

#### Detailed Answer:
- **Chain-of-Thought (CoT)**:
  - Generates reasoning traces solely within the internal parametric knowledge weights of the LLM.
  - Strengths: Low latency (single forward pass), does not require external runtime infrastructure or API tools.
  - Limitations: Subject to hallucinations, cannot access up-to-date data, cannot execute arithmetic or verify intermediate facts against real-world systems.
- **ReAct (Reasoning + Acting)**:
  - Interleaves explicit internal thoughts with external tool calls (actions) and external environment feedback (observations).
  - Thoughts help the model induce, track, and update action plans, adjust search strategies, and detect edge cases.
  - Actions ground the reasoning by retrieving live documentation, executing code/math, or modifying database state.
- **Decision Criteria**:
  - Use **CoT** for closed-world reasoning tasks (e.g. logic puzzles, creative writing, text summarization).
  - Use **ReAct** for knowledge-intensive search, multi-hop question answering, math evaluation, and autonomous workflows interfacing with APIs and databases.

---

### Q2: How do you prevent autonomous agents from getting trapped in infinite loops or hallucinating tool arguments?

#### Detailed Answer:
1. **Hard Guardrails (Step Limits & Timeouts)**:
   - Enforce strict `max_iterations` (e.g., 5-8 steps) and per-step wall-clock timeouts.
2. **Deterministic Schemas & Pydantic Validation**:
   - Enforce structured tool arguments using JSON Schema / Pydantic models. If the LLM generates invalid parameters, catch the `ValidationError` and feed the schema error back to the agent as an observation.
3. **Loop Detection & State Hashing**:
   - Hash each `(tool_name, arguments)` tuple. If the identical tool call is triggered twice in succession with the same output, intervene with a system warning prompting the agent to change its search strategy.
4. **Self-Reflection / Critic Step (Reflexion Pattern)**:
   - After each observation, require the agent to generate an intermediate reflection: *"Did this tool output answer the sub-question? What information is still missing?"*

---

### Q3: Why is standard Python `eval()` unsafe for LLM tool calling, and how does AST parsing solve this security vulnerability?

#### Detailed Answer:
- **The Danger of `eval()`**:
  - `eval()` compiles and executes arbitrary Python code in the runtime environment.
  - An attacker or prompt injection attack could trick the LLM into invoking:
    `eval("__import__('os').system('rm -rf /')")` or reading environment API keys.
- **The Safe AST (Abstract Syntax Tree) Solution**:
  - Using `ast.parse(expression, mode='eval')`, the expression is converted into a structured syntax tree without execution.
  - A custom visitor traverses the tree and strictly checks that node types are whitelisted (e.g., `ast.BinOp`, `ast.Add`, `ast.Mult`, `ast.Constant`).
  - Any node involving imports, attribute access (`__dict__`), or unauthorized function calls raises an immediate `ValueError`, completely neutralizing code injection.

---

### Q4: In Graph Retrieval-Augmented Generation (GraphRAG), how does knowledge graph traversal differ from naive dense vector semantic search?

#### Detailed Answer:
- **Vector RAG (Local Retrieval)**:
  - Embeds document chunks into high-dimensional vector space (e.g., 1536-dim).
  - Performs Cosine / Dot-Product Nearest Neighbor search (k-NN) using FAISS/ChromaDB.
  - Excels at finding isolated specific facts ("What was the Q3 revenue of Company X?").
  - Fails on **global multi-hop sensemaking** questions ("What are the top recurring architectural challenges across all projects in the last 5 years?").
- **GraphRAG (Global & Relational Retrieval)**:
  - Extracts entities (nodes) and relationships (edges) to construct a comprehensive knowledge graph.
  - Employs community detection algorithms (e.g., Leiden or Louvain) to partition the graph into hierarchical semantic clusters.
  - Generates pre-computed community summaries for macro-level questions and traverses graph edges for multi-hop relational queries.

---

### Q5: How do Mixture-of-Experts (MoE) architectures like DeepSeek-V3 achieve high parameter counts while maintaining low inference latency and compute cost?

#### Detailed Answer:
1. **Sparse Activation vs Dense Activation**:
   - In dense models (e.g., LLaMA-3 70B), every single parameter is active and evaluated for every input token.
   - In sparse MoE models (e.g., DeepSeek-V3 671B), the feed-forward network (FFN) layers are divided into multiple distinct "expert" subnetworks.
   - For each token, a gating/router network dynamically routes the token to only top-$K$ experts (e.g., top-8 out of 256 routed experts + 1 shared expert).
   - Only **37B parameters** are activated per token out of **671B total parameters**.
2. **Computational & Memory Trade-offs**:
   - **FLOPs / Latency**: The compute cost per token matches that of a 37B parameter model.
   - **Capacity / Knowledge**: The parameter capacity matches that of a 671B model, vastly improving factual knowledge and reasoning depth.
   - **Memory Footprint**: All 671B weights must reside in GPU VRAM (or fast host RAM), requiring techniques like Multi-Head Latent Attention (MLA) and FP8 quantization.
