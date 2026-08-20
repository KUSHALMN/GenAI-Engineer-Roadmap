# Day 19 — Recruiter & Behavioral Interview Preparation

Structured behavioral, system-ownership, and recruiter screening questions for AI & GenAI Engineer roles (STAR method).

---

### Q1: "Can you tell me about a project where you built an AI Agent or integrated Function Calling?"
**Suggested STAR Response Framework:**
- **Situation:** "In my recent project, our application needed to provide customer support that could look up live order statuses and calculate refund eligibility rather than giving generic static advice."
- **Task:** "I was tasked with building an AI assistant that could interface with internal microservices securely and reliably without hallucinatory actions."
- **Action:** "I implemented an OpenAI-compatible function calling architecture with strict Pydantic schemas. I integrated a dynamic tool registry that handles schema generation, argument validation, and error feedback loops. To ensure safety, I built sandboxed execution environments and implemented human-in-the-loop approvals for destructive operations."
- **Result:** "The assistant successfully handled 85% of tier-1 support queries autonomously with zero unauthorized data mutations, reducing average resolution time from 15 minutes to under 30 seconds."

---

### Q2: "How do you manage LLM API costs and latency when deploying agentic workflows to production?"
**Key Talking Points:**
1. **Model Routing / Tiering:** Route simple classification and extraction tasks to smaller, faster models (e.g., LLaMA 3.3 8B, GPT-4o-mini) and reserve large flagship models (GPT-4o, Claude 3.5 Sonnet) only for complex multi-tool planning.
2. **Prompt Caching:** Utilize provider prompt caching (OpenAI/Anthropic/Groq) for repetitive tool schemas and system instructions to cut latency by 50-80% and token costs by up to 90%.
3. **Parallel Tool Calls:** Enable parallel tool calling rather than sequential turns to reduce total API round trips.
4. **Semantic Caching:** Cache common tool outputs and deterministic responses using Redis or vector cache.

---

### Q3: "How do you handle rate limits, network failures, or flaky third-party tools in an agent loop?"
**Key Talking Points:**
1. **Exponential Backoff & Retries:** Implement robust retry policies with jitter for LLM API calls and external tool HTTP endpoints.
2. **Graceful Fallbacks:** If a tool call fails, feed the error back to the agent so it can attempt an alternative tool or apologize politely with fallback guidance.
3. **Loop Circuit Breakers:** Always configure `max_iterations` (e.g., 5-10) and total timeout bounds to prevent infinite tool-calling loops and runaway billing.
