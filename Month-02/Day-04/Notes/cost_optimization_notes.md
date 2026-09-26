# 💰 LLM Caching & Cost Optimization Notes

## 1. Why LLM Caching Matters

In high-throughput GenAI systems:
- **Cost**: Repeated queries (e.g., FAQ, common agent queries, system prompts) waste thousands of dollars in input and output tokens.
- **Latency**: LLM calls take between 300ms to 5,000ms. An in-memory cache hit returns in `< 1ms` (up to 1000x faster).
- **Rate Limits & Reliability**: Caching absorbs traffic spikes, shielding rate limits on providers like OpenAI, Anthropic, or Groq.

---

## 2. Caching Strategies Compared

| Strategy | Lookup Speed | Match Precision | Failure Mode | Best For |
|---|---|---|---|---|
| **Exact Match (Deterministic Key)** | `< 0.5ms` (Hash table) | 100% Deterministic | Cache miss on minor punctuation change | Zero-temperature completions, summarization, extraction |
| **Semantic Cache (Vector Similarity)** | `10ms - 50ms` (Vector DB) | Approximate (Threshold e.g. 0.92) | False positives (returning stale or semantically mismatched answers) | Broad customer support FAQ, exploratory search |
| **Prompt Prefix Caching** | Upstream provider | 100% Deterministic | Provider-dependent discount (e.g., Anthropic / OpenAI 50% discount) | Long static system prompts, large document contexts |

---

## 3. Deterministic Key Generation Best Practices

1. **Whitespace & Case Normalization**: Strip leading/trailing whitespaces, normalize lowercase for model names and role definitions.
2. **Key Ordering**: Always sort keys alphabetically when serializing JSON objects (`json.dumps(..., sort_keys=True)`).
3. **Float Precision**: Round temperature and top_p (e.g., `round(temp, 4)`) to prevent floating-point representation differences across platforms.
4. **Temperature Consideration**:
   - Queries with `temperature == 0.0` are safe for long TTLs (days or weeks).
   - Queries with `temperature > 0.5` are stochastic; caching them should only occur if the user intentionally desires reproducible responses or explicitly enables session caching.

---

## 4. TTL & Invalidation Patterns

- **Time-To-Live (TTL)**:
  - Static Knowledge: 24h - 7 days.
  - User-specific data: 1h - 4h.
  - Ephemeral agent loops: 5 - 15 minutes.
- **Cache Eviction**:
  - LRU (Least Recently Used) ensures a fixed memory footprint.
  - Active sweep on background thread or passive sweep on access.

---

## 5. Token Savings Calculation Formula

$$\text{Cost Saved} = \sum_{\text{hits}} \left( \frac{\text{Tokens Saved}}{1000} \times \text{Rate}_{\text{model}} \right)$$

$$\text{Latency Saved} = \sum_{\text{hits}} (\text{Original Latency} - \text{Cache Lookup Latency})$$
