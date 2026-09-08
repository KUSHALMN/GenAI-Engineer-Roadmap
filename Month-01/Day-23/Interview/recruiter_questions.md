# 💼 Day 23 Recruiter & System Architecture Interview Questions

### 1. "Can you walk me through how you engineered low-latency LLM streaming in production?"
**Talking Points**:
- "When we architected our conversational AI interface, TTFT was our primary SLA. End users were waiting up to 6 seconds for complete answers, which caused user drop-off.
- I introduced asynchronous Server-Sent Events (SSE) streaming with FastAPI. By leveraging Python's `asyncio` event loop and streaming token generators, we reduced the perceived response time to under 450ms.
- We also instituted client disconnection handling to prevent zombie inferences from burning GPU tokens after users navigated away."

### 2. "Why choose FastAPI over Flask or Django for GenAI streaming endpoints?"
**Talking Points**:
- FastAPI is natively built on top of Starlette and ASGI (Asynchronous Server Gateway Interface), utilizing Python's `async/await` syntax.
- Flask (WSGI) traditionally relies on synchronous worker threads (or gevent/greenlets), where long-lived streaming connections tie up thread pools.
- FastAPI allows a handful of ASGI worker processes to manage thousands of concurrent open HTTP streaming connections simultaneously.
