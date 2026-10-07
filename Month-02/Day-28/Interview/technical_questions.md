# 🎯 Day 28 Technical Interview Questions & Answers

## 1. How does LLM Grammar-Constrained Decoding / JSON Schema enforcement work at the inference engine level (e.g. Outlines, vLLM)?
**Answer:**
Standard LLMs sample next tokens from the vocabulary probability distribution $P(w_t | w_{<t})$.
In Grammar-Constrained Sampling:
1. The JSON Schema is parsed into a **Context-Free Grammar (CFG)** or a **Deterministic Finite Automaton (DFA)**.
2. At each token step $t$, the DFA computes the exact set of allowable valid tokens (e.g., if inside a string literal awaiting a closing quote, numeric tokens or syntax violating characters receive probability $-\infty$).
3. The model's logits are masked *before* softmax sampling, mathematically guaranteeing 100% syntactically valid JSON without requiring post-hoc regex repairs or retry loops.

---

## 2. What are the key failure modes of Function Calling / Tool Dispatchers, and how do you design for resilience?
**Answer:**
Key failure modes:
1. **Hallucinated Tool Name**: Model invokes a tool not present in the catalog.
   - *Defense*: Strict dictionary lookup in `ToolDispatcher` with fallbacks and clarifying prompts.
2. **Missing or Extra Parameters**: Model forgets required arguments or invents fictional keys.
   - *Defense*: Pydantic schema validation before invocation.
3. **Type Coercion Failures**: Passing string `"500"` when integer `500` is expected.
   - *Defense*: Automatic casting layers and lenient deserialization.
4. **Tool Execution Errors**: Upstream API failures inside the tool.
   - *Defense*: Return structured error payloads `{"success": false, "error": "..."}` back to the LLM context so the agent can self-correct.

---

## 3. Compare Trie vs. Hash Table for string prefix lookups and autocomplete.
**Answer:**
- **Hash Table**: $O(L)$ exact lookup where $L$ is word length. However, finding all strings with prefix $P$ requires scanning the entire table of $N$ keys ($O(N \cdot L)$), making real-time autocomplete computationally expensive.
- **Trie (Prefix Tree)**:
  - Locates the prefix root in $O(|P|)$ operations.
  - Collects all $K$ matching descendants in $O(\text{matched tokens})$.
  - Shares common prefixes, significantly reducing memory footprint when storing dictionaries with dense overlapping prefixes (e.g., english dictionaries, code symbol indexes).
