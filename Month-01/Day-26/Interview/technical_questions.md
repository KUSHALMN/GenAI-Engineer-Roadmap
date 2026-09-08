# 🎯 Day 26 Technical Interview Questions: Guardrails & Model Fallbacks

### Q1: What is the "Thundering Herd" problem in LLM retries and how does Full Jitter solve it?
**Answer**:
When an LLM provider experiences a temporary outage or rate limit spike, all queued client requests fail concurrently. If clients use deterministic exponential backoff ($2, 4, 8 \text{ sec}$), all clients retry in synchronized bursts at the exact same second, immediately re-overwhelming the provider.
- **Full Jitter**: Computes sleep time as $t = \text{random}(0, \min(\text{max\_delay}, \text{base\_delay} \times 2^{\text{attempt}}))$. This flattens the retry curve into a smooth uniform distribution, allowing the provider's token bucket or queue to recover cleanly.

---

### Q2: How do you design a model fallback cascade without degrading user experience?
**Answer**:
1. **Context Window Alignment**: Ensure the fallback model has sufficient context length to accept the prompt and RAG context passed to the primary model.
2. **Schema Uniformity**: Standardize system instructions across both models so that tool calls and structured JSON schemas are identically produced.
3. **Telemetry Tagging**: Tag the response with `x-model-served: fallback`, notifying analytics dashboards of the primary model's degradation while giving the end-user uninterrupted service.
