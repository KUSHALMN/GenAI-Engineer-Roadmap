# 📝 Day 25 Study Notes: Structured Outputs, Schema Enforcement & JSON Repair

## 1. The Challenge with Raw Text Outputs
When integrating LLMs into software architectures, raw natural language responses cannot be safely consumed by databases, microservices, or frontend components.
Common failure modes:
1. Markdown enclosures: \`\`\`json { ... } \`\`\`
2. Hallucinated keys or altered camelCase/snake_case formatting.
3. Unquoted strings, trailing commas, or truncated closing brackets due to token limits.
4. Semantic type violations (e.g. string "twenty" instead of integer 20).

## 2. Techniques for Structured Extraction
| Approach | Mechanism | Pros | Cons |
|---|---|---|---|
| **Prompt Instruction Only** | "Output pure JSON with schema X" | Zero framework dependency | High rate of formatting failure (5-15%) |
| **JSON Mode** | Enforces valid JSON tokens via logit biasing | Guarantees syntactically valid JSON | Does not guarantee specific schema keys |
| **Tool / Function Calling** | Model generates arguments conforming to JSON Schema | High schema conformity | Model may emit explanations outside arguments |
| **Grammar-based Decoding** (e.g., Outlines, GBNF) | Direct token logit masking against context-free grammar | 100% mathematical guarantee of valid schema | Requires local/engine-level access (vLLM/llama.cpp) |
| **Pydantic + Auto-Repair + Retry Loop** | Parse, clean, repair, and feedback validate | Works across all closed & open-source APIs | Incurs retry latency on validation error |

## 3. The Instructor Pattern
If `pydantic.ValidationError` occurs:
1. Extract the exact field path (`loc`) and human-readable failure message (`msg`).
2. Construct a targeted follow-up prompt:
   *"Your previous output failed validation on field 'total_price': Total price 120 does not match expected 100 (qty 2 * price 50). Please correct only this schema violation."*
3. Retry with exponential backoff (typically succeeding in 1 retry).
