# 📝 Notes — Day 18: OpenTelemetry Tracing & LRU Cache Design

## 1. GenAI Observability Attributes
- `gen_ai.system`: e.g. "openai", "vllm", "bedrock".
- `gen_ai.request.model`: e.g. "llama-3-8b-instruct".
- `gen_ai.usage.prompt_tokens`: Count of prompt tokens.
- `gen_ai.usage.completion_tokens`: Count of generated tokens.
