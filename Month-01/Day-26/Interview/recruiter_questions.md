# 💼 Day 26 Recruiter & System Architecture Interview Questions

### 1. "How do you protect production GenAI systems from prompt injection and data exfiltration?"
**Talking Points**:
- "We implement a strict multi-layer defense in depth:
  1. Input Guardrails scan for jailbreak heuristics, roleplay override attempts, and dangerous system tokens.
  2. PII Masking redacts social security numbers, credit card numbers, and API keys before transmission to third-party model providers.
  3. Context Isolation clearly separates user instructions from external untrusted RAG retrieved text using XML tags.
  4. Output Guardrails verify that responses do not contain leaked secrets, toxic statements, or hallucinated PII."

### 2. "How do you handle high 429 rate limit spikes from third-party LLM providers?"
**Talking Points**:
- "We use exponential backoff with full jitter to avoid harmonic thundering-herd retry storms.
- If retries fail or if an outage occurs, our gateway transparently fails over to a secondary fallback provider (e.g. switching from OpenAI to Anthropic or self-hosted vLLM on AWS).
- We maintain circuit breakers with error rate thresholds to fast-fail traffic and avoid degraded thread pools."
