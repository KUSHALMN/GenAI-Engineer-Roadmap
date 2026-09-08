# 🎯 Day 23 Technical Interview Questions: LLM Streaming & Async APIs

### Q1: How does Server-Sent Events (SSE) differ from WebSockets in GenAI architectures?
**Answer**:
- **SSE**: Uses regular HTTP/1.1 or HTTP/2 transport with `Content-Type: text/event-stream`. It is unidirectional (server-to-client). Because it is standard HTTP, it traverses firewalls, load balancers, and CDN edge proxies without special protocol upgrades. It natively supports automatic browser reconnection (`Last-Event-ID`). Perfect for typical LLM chat applications where user messages are standard POST requests and answers are streaming tokens.
- **WebSockets**: Initiated via an HTTP 101 Switching Protocols handshake, upgrading to a persistent, full-duplex TCP connection. Ideal when low-latency client-to-server messaging is needed simultaneously (e.g. streaming audio speech-to-speech models, mid-generation user cancellations, or live collaborative cursors).

---

### Q2: What is Time To First Token (TTFT) and what factors contribute to it?
**Answer**:
TTFT is the latency from user request submission until the first generated token arrives at the client.
Key factors include:
1. **Network latency & TLS handshake**.
2. **Gateway middleware overhead** (authentication, rate-limiting, semantic cache check, prompt-guardrail validation).
3. **Prompt prefill phase (KV-cache computation)**: Processing the prompt tokens through transformer attention layers in parallel. Longer prompts (e.g., 32k RAG context) dramatically increase TTFT.
4. **Queue wait time** in the GPU inference engine batch scheduler.

---

### Q3: What happens when an HTTP client disconnects prematurely while an LLM is streaming?
**Answer**:
Without proper handling, the server might continue calling the LLM backend, wasting GPU compute and inference tokens. In FastAPI/Starlette, disconnecting triggers an `asyncio.CancelledError` inside the generator. Production systems catch this cancellation and explicitly call the inference engine's cancellation hook (e.g., `client.abort()` or canceling the underlying `asyncio.Task`) to release GPU memory and stop token burn.
