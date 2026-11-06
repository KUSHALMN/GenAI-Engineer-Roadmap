# Day 26: Technical Interview Preparation — Observability & Rolling Hash

### Q1: What semantic conventions (attributes) should every agent span record in OpenTelemetry?
**Answer:**
- `gen_ai.system`: e.g. "langgraph", "autogen", "custom_mcp"
- `gen_ai.prompt.tokens` / `gen_ai.completion.tokens`: Token consumption
- `gen_ai.tool.name` & `gen_ai.tool.arguments`: Parameters executed
- `gen_ai.cost.usd`: Estimated monetary spend
- `gen_ai.correlation_id`: End-to-end user request ID

### Q2: Why is collision verification mandatory in Rabin-Karp?
**Answer:**
Because hash functions map an infinite domain of strings into a finite integer modulus (`PRIME`), two different strings can produce identical hash values (hash collision). Verifying the substring character-by-character on a hash match guarantees 100% accuracy.
