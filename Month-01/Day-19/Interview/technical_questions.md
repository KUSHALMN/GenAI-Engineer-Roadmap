# Day 19 — Technical Interview Questions: LLM Tool & Function Calling

Comprehensive interview questions and detailed answers targeting GenAI Engineer and AI Systems roles.

---

### Q1: How does LLM Function Calling (Tool Calling) work under the hood?
**Answer:**
1. **Schema Injection:** The developer supplies tool definitions (JSON Schema format specifying function names, descriptions, parameters, types, and required fields) alongside the conversation prompt.
2. **Constrained Decoding / Specialized Training:** Modern models (GPT-4o, LLaMA 3.3, Claude 3.5 Sonnet) have been fine-tuned on function calling tokens. When the model determines external data/action is required, it outputs a structured JSON token stream matching the schema rather than conversational text, along with a `finish_reason: "tool_calls"`.
3. **Client-Side Execution:** The application parses the tool call ID, function name, and JSON arguments, then dispatches execution to the corresponding local or API function.
4. **Context Injection:** The tool's output is wrapped in a message with `role: "tool"` and the identical `tool_call_id`, then sent back to the LLM.
5. **Synthesis:** The LLM receives the execution result as part of its context and generates the final natural language answer for the user.

---

### Q2: What is the difference between JSON Mode and Tool / Function Calling?
**Answer:**
- **JSON Mode:** Guarantees that the LLM's raw text completion is syntactically valid JSON. However, it does not validate against a specific schema nor does it provide structured metadata (`tool_calls` array, IDs) for automated agent loops.
- **Function / Tool Calling:** The model is trained to actively decide *which* tool to call (or multiple tools in parallel), populates specific parameters adhering strictly to the JSON schema, and emits distinct message payload structures designed for agentic loops.

---

### Q3: How do you handle LLM hallucinations or schema validation errors during tool calling?
**Answer:**
1. **Pydantic Validation:** Wrap argument deserialization inside Pydantic models.
2. **Error Feedback Loop (Self-Correction):** If deserialization or execution throws an exception (e.g., missing parameter or type mismatch), send the error message directly back to the LLM with `role: "tool"` (e.g., `"Error: 'limit' must be an integer > 0"`). LLMs excel at self-correcting on subsequent iterations.
3. **Structured Outputs (Grammar-Constrained Decoding):** Use libraries or API features like OpenAI Structured Outputs, Outlines, or Instructor that constrain the token logits directly at generation time, preventing syntax or type violations with 100% reliability.

---

### Q4: How do Parallel Tool Calling and Multi-Step Agent Loops differ?
**Answer:**
- **Parallel Tool Calling:** The LLM generates multiple tool invocations in a single completion step when subtasks are independent (e.g., fetching weather for Tokyo, London, and Paris simultaneously). All calls can be dispatched concurrently via `asyncio.gather()`.
- **Multi-Step Agent Loops (ReAct / Sequential):** When task B depends on the output of task A (e.g., searching database for user ID -> then calculating account balance for that ID), the loop must execute iteratively across multiple LLM turns.

---

### Q5: What security risks are introduced with Tool Calling, and how do you mitigate them?
**Answer:**
1. **Indirect Prompt Injection:** Malicious text returned from external tools (e.g., web scrapers, database rows, email contents) may contain prompt injection instructions hijacking the agent.
   - *Mitigation:* Treat tool outputs as untrusted data; apply strict system instructions and sandwich prompting; use separate LLM evaluators.
2. **Arbitrary Code Execution / Unsafe Eval:** Using `eval()` or unsanitized shell executions for calculator or terminal tools.
   - *Mitigation:* Use AST-based parsers, sandboxed containers (e.g., Docker, gVisor, WebAssembly), and least-privilege API tokens.
3. **Destructive Actions (Human-in-the-loop):** Accidental deletions or financial transactions.
   - *Mitigation:* Require explicit user confirmation before executing irreversible or sensitive tool calls.
