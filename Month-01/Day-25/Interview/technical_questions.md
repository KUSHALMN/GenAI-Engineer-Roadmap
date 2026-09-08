# 🎯 Day 25 Technical Interview Questions: Structured Outputs & JSON Validation

### Q1: How do constrained decoding (grammar masks) and post-generation validation differ?
**Answer**:
- **Constrained Decoding (GBNF / Outlines / vLLM)**: Masks the softmax logits at every token generation step so that only tokens consistent with the JSON context-free grammar can be sampled.
  - *Advantage*: 100% syntactically valid JSON guaranteed on the first pass; zero parse failures.
  - *Disadvantage*: Does not validate cross-field business logic (e.g., $qty \times price = total$), requires direct inference engine access.
- **Post-Generation Validation (Pydantic / Instructor)**: The LLM generates text freely, and a validation pipeline (Pydantic V2) verifies syntax and complex semantic invariants.
  - *Advantage*: Can enforce regex, range limits, and inter-field dependencies. Works across black-box APIs.
  - *Disadvantage*: Incurs retry latency when generation fails.

---

### Q2: What is the optimal retry strategy when an LLM violates a Pydantic schema?
**Answer**:
1. Do not simply re-send the original prompt (the model will often repeat the same error due to high temperature/system bias).
2. Append the previous malformed JSON and the exact `ValidationError` trace into the conversation history:
   `"Your previous response had error: Field 'customer_email' must be a valid email address. Received: 'none'. Fix this error and return valid JSON."`
3. Set max retries to 2 or 3. If still failing, fall back to a deterministic heuristic or route to human review.
