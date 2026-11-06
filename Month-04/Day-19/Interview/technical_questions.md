# Day 19: Technical Interview Preparation — LLM-MCP Bridges & DAG DP

### Q1: Why is an intermediate bridge layer necessary between LLMs and MCP servers?
**Answer:**
Model providers (OpenAI, Anthropic, Gemini, Mistral) have subtle syntax variances for function definitions and tool call blocks. The LLM-MCP bridge translates standard MCP JSON-RPC schemas into provider-specific payloads, decoupling agent application code from backend tool implementations.

### Q2: Why is the Longest Path problem polynomial in a DAG but NP-Hard in a general graph?
**Answer:**
In general graphs with positive cycles, paths can be infinitely long. In a DAG, topological order guarantees edges only point forward. Subproblems have a strict partial ordering with no cycles, allowing dynamic programming to compute the longest path in linear $O(V + E)$ time.
