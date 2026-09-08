# 📝 Day 26 Study Notes: Error Handling, Guardrails & Model Fallbacks

## 1. The Anatomy of GenAI Failure Modes
In production, LLM services experience unique failure categories:
1. **Network & Infrastructure**: Timeouts, connection resets, TCP packet loss.
2. **Provider Rate Limiting (HTTP 429)**: Token per minute (TPM) or Request per minute (RPM) exhaustion.
3. **Safety & Content Filter Rejections**: Upstream provider safety filter stops completion mid-stream.
4. **Adversarial Exploitation**: Prompt injections, jailbreaks, and sensitive data extraction.

## 2. Guardrails Architecture
A defense-in-depth guardrails system operates symmetrically:
- **Input Guardrails**:
  - *Pattern Scanners*: Regex for delimiter attacks ("Ignore previous instructions", "system override").
  - *PII Redaction*: Mask SSNs, credit cards, emails before sending to external model providers.
  - *Embedding Classification*: Fast cosine classifier against known toxic/harmful vector clusters.
- **Output Guardrails**:
  - *Secret Leak Prevention*: Ensure internal API keys, passwords, or connection strings are never emitted.
  - *Factuality / Hallucination Checks*: Grounding alignment against retrieved source documents.

## 3. Resilience: Retries, Jitter & Fallback Cascades
- **Why Exponential Backoff Needs Jitter**: If 500 requests hit rate limits simultaneously at $t_0$, retrying at strictly $t_0 + 2^k$ causes synchronized harmonic waves ("thundering herd"). Adding uniform random jitter ($U(0, \text{delay})$) disperses retry spikes across time.
- **Fallback Cascades**:
  - Frontier Model (Primary): GPT-4o / Claude 3.5 Sonnet.
  - Fallback Model: LLaMA-3.3 70B (self-hosted vLLM) or GPT-4o-mini.
  - Graceful Degradation: Inform the client or trigger cached responses if both fail.
