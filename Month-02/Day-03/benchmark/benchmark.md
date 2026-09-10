# Agent Benchmark — Day 33 (Month 02, Day 03)
## LangChain Tool-Calling Agent with Groq LLaMA3-8B

---

## Test Queries & Results

| Query | Tool Used | Latency (ms) | Correct? |
|-------|-----------|-------------|----------|
| `What is 15 * 24 + 100?` | `calculator_tool` | ~320 | ✅ 460 |
| `What is the weather in Bangalore?` | `weather_tool` | ~410 | ✅ 22°C |
| `Search for LangChain agents tutorial` | `search_tool` | ~380 | ✅ Results |
| `What is 2 to the power of 10?` | `calculator_tool` | ~290 | ✅ 1024 |
| `Tell me a joke` | None (direct LLM) | ~250 | ✅ |

---

## Latency Breakdown

```
Total agent latency = LLM planning + Tool execution + LLM synthesis

LLM planning (tool selection):  ~200-300ms  (Groq ultra-fast inference)
Tool execution (stub):          ~1-5ms
LLM synthesis (final answer):   ~150-200ms
─────────────────────────────────────────
Total:                          ~350-500ms per query
```

---

## Tool Selection Accuracy

| Scenario | Expected Tool | Agent Selected | Match |
|----------|--------------|----------------|-------|
| Math expression | calculator | calculator | ✅ |
| City weather | weather | weather | ✅ |
| General knowledge | search | search | ✅ |
| Conversational | none | none | ✅ |

Tool selection accuracy: **100%** on test set (4/4)

---

## Token Usage (Groq LLaMA3-8B)

| Phase | Avg Tokens |
|-------|-----------|
| System prompt | 45 |
| User query | 12 |
| Tool schema injection | 180 |
| Agent scratchpad | 60 |
| Final answer | 35 |
| **Total per query** | **~332** |

---

## Observations

1. **Tool schema size** is the biggest token cost — 180 tokens for 3 tool schemas.
2. **Groq latency** is ~5x faster than OpenAI for same model size due to custom LPU hardware.
3. **max_iterations=5** prevents infinite loops; most queries resolve in 1-2 steps.
4. **Safe eval** for calculator avoids `eval()` injection — critical for production.

---

## Recommendations

- Cache tool schemas in system prompt to avoid re-injection per turn.
- Add tool result caching (Redis) for repeated weather/search queries.
- Use `return_intermediate_steps=True` for observability and debugging.
