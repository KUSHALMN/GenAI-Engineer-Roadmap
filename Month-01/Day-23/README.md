# 📅 Day 23: ⚡ LLM Streaming + Async APIs & LRU Cache DSA

Welcome to **Day 23** of the **GenAI Engineer Roadmap**! Today focuses on building production-grade asynchronous token streaming APIs using FastAPI, Server-Sent Events (SSE), WebSockets, tracking Time To First Token (TTFT), and mastering the LeetCode 146 LRU Cache problem in Java.

---

## 📁 Day 23 Project Structure

```
Day-23/
├── AI/
│   └── streaming-llm-api/
│       ├── src/
│       │   ├── app.py              # FastAPI endpoints for SSE, JSONL & WebSockets
│       │   ├── stream_engine.py    # Async token stream simulator & latency tracker
│       │   └── schemas.py          # Pydantic models for streaming contracts
│       ├── tests/
│       │   └── test_streaming.py   # Pytest unit & integration tests
│       ├── requirements.txt
│       └── README.md
│
├── src/
│   ├── app.py
│   ├── stream_engine.py
│   └── schemas.py
├── tests/
│   └── test_streaming.py
│
├── DSA/
│   └── lru_cache.java              # LeetCode 146: LRU Cache (HashMap + Doubly Linked List)
│
├── Interview/
│   ├── technical_questions.md       # SSE vs WebSockets, TTFT, cancellation
│   ├── coding_questions.md          # LRU Cache design nuances & concurrency
│   └── recruiter_questions.md       # Production latency optimization talking points
│
├── Notes/
│   └── day23_notes.md
├── Resources.md
└── README.md
```

---

## ⚡ Core Concepts Learned

1. **Server-Sent Events (SSE)**: Unidirectional, firewall-friendly token streaming over standard HTTP with `text/event-stream`.
2. **TTFT Optimization**: Dissecting prompt prefill vs autoregressive decode latency.
3. **Async Event-Loop Concurrency**: Handling hundreds of concurrent streams without blocking worker threads.
4. **LRU Cache Implementation**: Achieving $O(1)$ operations via HashMap and custom Doubly Linked List.

---

## 🚀 Execution Commands

### Test Python Streaming API
```bash
pytest Month-01/Day-23/tests/test_streaming.py -v
```

### Run Java LRU Cache Solution
```bash
javac Month-01/Day-23/DSA/lru_cache.java
java -cp Month-01/Day-23/DSA lru_cache
```
