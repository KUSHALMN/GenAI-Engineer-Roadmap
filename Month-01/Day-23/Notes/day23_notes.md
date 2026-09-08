# 📝 Day 23 Study Notes: LLM Streaming, Async APIs & High-Throughput Architectures

## 1. Why LLM Streaming Matters
In traditional REST request-response cycles, the client waits for the entire completion before receiving any bytes. For a 500-token completion generated at 25 tokens/sec:
- **Blocking request latency**: ~20 seconds before the user sees anything.
- **Streaming response latency**: Time To First Token (TTFT) ~ 300ms - 800ms.
Human reading speed is approximately 5 to 7 words per second. By streaming tokens as soon as the model yields them, the user begins reading immediately, dramatically improving perceived latency.

## 2. Streaming Protocols: SSE vs. WebSockets vs. gRPC
| Dimension | Server-Sent Events (SSE) | WebSockets | gRPC Streaming |
|---|---|---|---|
| **Direction** | Unidirectional (Server -> Client) | Bidirectional (Full Duplex) | Bidirectional / Client / Server |
| **Transport** | Standard HTTP/1.1 or HTTP/2 | Upgraded TCP connection | HTTP/2 binary framing (Protobuf) |
| **Firewall / Proxies** | Zero special proxy config needed | Requires reverse proxy upgrade | Requires HTTP/2 ingress |
| **Reconnection** | Native browser retry built-in | Must be handled in JS | Client interceptors / channel retry |
| **Best Used For** | Standard LLM chat completion | Audio/voice streams, live interruptions | Internal microservices & RPC |

## 3. Key Latency Metrics in Production GenAI
- **Time To First Token (TTFT)**: Time elapsed from when the HTTP request hits the gateway until the first token byte is sent. Reflects model prefill time, network hop, and prompt tokenization.
- **Inter-Token Latency (ITL)**: Time elapsed between subsequent tokens during the autoregressive decode phase.
- **Tokens Per Second (TPS)**: Total completion tokens divided by total generation duration.

## 4. Concurrency & Async I/O in Python
Because LLM API calls are I/O bound (waiting on GPU inference servers or third-party APIs like OpenAI, Anthropic, or vLLM), Python's `asyncio` event loop allows a single process to multiplex thousands of active connections without thread overhead. Using async generators (`async def ... yield ...`) avoids buffering chunks in RAM.
