# Day 03 Notes: Tool Selection and Routing

## 1. Routing Strategies in Production
1. **Rule-Based Prefix/Regex:** Ultra-fast filter for explicit commands (e.g., `/search`, `calc:`).
2. **Semantic Vector Search:** Embed tool descriptions into a vector store; cosine match user query against tool embeddings.
3. **Multi-Model Cascading:** Use a tiny 1B parameter model (e.g. Llama-3.2-1B / Gemma-2B) as a dedicated tool selector before passing context to larger reasoning engines.

## 2. Handling Ambiguity and Unsupported Queries
Always provide an explicit escape route:
- If confidence < threshold: Trigger a clarification dialog or route to general LLM conversational fallback.
