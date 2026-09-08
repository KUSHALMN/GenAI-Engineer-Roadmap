# 📓 Learning Journal

> Daily log of progress, wins, struggles, and insights.

---

## Month 01

### Day 01
- **Date:** Day 1
- **Topics:** AI/ML/GenAI basics, LLM, Transformers, Python OOP, DSA (HashMap)
- **What I built:** Terminal chatbot using Groq API (LLaMA 3.3 70B)
- **Key insight:** LLMs process prompts via tokenization → attention → output generation
- **Struggled with:** Understanding attention mechanism
- **Tomorrow's goal:** Learn NLP basics and embeddings

---

### Day 02
- **Date:** Day 2
- **Topics:** NLP, Tokenization, Embeddings, ChromaDB, DSA (Two Pointers, Sliding Window)
- **What I built:** Embeddings demo, similarity checker, ChromaDB vector store
- **Key insight:** Text is just numbers — embeddings capture semantic meaning as vectors
- **Struggled with:** Understanding cosine similarity intuitively
- **Tomorrow's goal:** Learn RAG pipeline and chunking

---

### Day 03
- **Date:** Day 3
- **Topics:** RAG pipeline, Text chunking, Cosine similarity from scratch, PDF processing
- **What I built:** PDF similarity search using ChromaDB + Sentence Transformers
- **Key insight:** RAG = Chunk → Embed → Store → Retrieve → Generate
- **Struggled with:** Choosing the right chunk size and overlap
- **Tomorrow's goal:** Learn prompt engineering techniques

---

### Day 04
- **Date:** Day 4
- **Topics:** Prompt Engineering (Zero-shot, Few-shot, CoT, System Role), Binary Search
- **What I built:** AI Q&A bot with system prompt and conversation history
- **Key insight:** How you prompt the model is as important as the model itself
- **Struggled with:** Chain-of-thought prompting for complex reasoning
- **Tomorrow's goal:** Learn FastAPI and build AI chat API

---

### Day 05
- **Date:** Day 5
- **Topics:** FastAPI, Pydantic, REST APIs, Binary Search on Rotated Arrays
- **What I built:** Calculator API, AI Chat API with session-based history
- **Key insight:** FastAPI auto-generates Swagger docs — great for testing APIs instantly
- **Struggled with:** Session management for multi-user chat
- **Tomorrow's goal:** Continue building on FastAPI — add auth and database

---

### Day 06
- **Date:** Day 6
- **Topics:** SQL Basics, PostgreSQL, psycopg2, CRUD operations, DSA (HashMap & HashSet)
- **What I built:** Full CRUD user database with Python + PostgreSQL
- **Key insight:** SQL is the language of data — every AI app needs a database
- **Struggled with:** Managing DB connections and handling duplicate entries
- **Tomorrow's goal:** Learn LangChain basics and build an AI chain

---

### Day 07
- **Date:** Day 7
- **Topics:** PDF RAG Chatbot, Python Decorators, Interview Prep, DSA (Sliding Window, Greedy)
- **What I built:** Full PDF RAG Chatbot — pypdf + ChromaDB + Groq
- **Key insight:** A PDF RAG chatbot is the most practical GenAI portfolio project
- **Struggled with:** Choosing optimal chunk size for retrieval quality
- **Tomorrow's goal:** Learn LangChain and build an AI agent

---

### Day 08
- **Date:** Day 8
- **Topics:** Modular RAG architecture, Lazy loading, Binary Search DSA
- **What I built:** Refactored RAG chatbot — embedding.py, vector_store.py modules
- **Key insight:** Good code is modular code — single responsibility per file
- **Struggled with:** Managing global state across modules
- **Tomorrow's goal:** Add retriever and prompt builder modules

---

### Day 09
- **Date:** Day 9
- **Topics:** Full RAG pipeline, retriever with scores, Two Pointers DSA
- **What I built:** RAG chatbot with retriever.py, prompt_builder.py, rag_pipeline.py
- **Key insight:** Production RAG = 8 focused modules, not one script
- **Struggled with:** Distance scores interpretation in ChromaDB
- **Tomorrow's goal:** Add chain.py as LLM execution layer

---

### Day 10
- **Date:** Day 10
- **Topics:** Chain architecture, paragraph splitting, Stack DSA
- **What I built:** RAG chatbot with chain.py — full 9-module architecture
- **Key insight:** Stack = LIFO — perfect for bracket matching and min tracking
- **Struggled with:** Min Stack two-stack approach
- **Tomorrow's goal:** Learn LangChain basics

---

---

### Day 23
- **Topics:** ⚡ LLM Streaming + Async APIs, Server-Sent Events (SSE), WebSockets, TTFT Optimization, LRU Cache DSA (LeetCode 146)
- **What I built:** Asynchronous FastAPI token streaming service with TTFT metrics, client cancellation handling, and O(1) Java LRU Cache.
- **Key insight:** Streaming reduces perceived user latency from 6s to 400ms by pushing tokens as they are decoded.

---

### Day 24
- **Topics:** 🧠 Production Prompt Engineering, Few-Shot In-Context Learning, Chain-of-Thought (CoT), Automated Metrics (BLEU, ROUGE-L, Cosine Similarity), Word Break DSA (LeetCode 139)
- **What I built:** Versioned prompt template engine, automated quantitative evaluation harness, and Java Word Break DP/Trie solution.
- **Key insight:** Treat prompts as software with golden regression test suites and quantitative benchmarks.

---

### Day 25
- **Topics:** 📦 Structured Outputs + Pydantic V2, JSON Auto-Repair, Instructor Feedback Loop, Trapping Rain Water DSA (LeetCode 42)
- **What I built:** Pydantic V2 validation gateway with automatic markdown fence stripping, JSON bracket healing, and Java Two-Pointer Trapping Rain Water.
- **Key insight:** Never pass raw LLM text downstream; validate with strict schemas and feed back error traces for self-healing retries.

---

### Day 26
- **Topics:** 🛡️ Error Handling + Guardrails, Input/Output Safety Filters, PII Redaction, Exponential Backoff with Jitter, Model Fallback Cascades, Merge k Sorted Lists DSA (LeetCode 23)
- **What I built:** Multi-tier safety gateway, regex/heuristic injection blocker, full jitter backoff retry orchestrator, and Java Min-Heap Merge k Lists.
- **Key insight:** Jitter prevents the thundering-herd retry storm during provider rate limits.

---

### Day 27
- **Topics:** 🔍 LLM Observability, OpenTelemetry Distributed Spans, Latency Percentiles (p50/p95/p99), Token Accounting, Median of Two Sorted Arrays DSA (LeetCode 4)
- **What I built:** In-memory OpenTelemetry tracer, dollar cost calculator, percentile aggregator, and Java Binary Search Partition Median algorithm.
- **Key insight:** Mean latency hides catastrophic tail spikes; monitor p95 and real-time dollar cost attribution.

---

### Day 28
- **Topics:** 🔐 GenAI Security, OWASP Top 10 for LLMs, Prompt Injection Firewall, Canary Token Tripwires, Word Ladder DSA (LeetCode 127)
- **What I built:** Security proxy detecting delimiter spoofing, Base64 obfuscations, canary token leaks, and Java Bidirectional BFS Word Ladder.
- **Key insight:** Canary tokens act as active tripwires detecting confidential prompt extraction before response delivery.

---

### Day 29
- **Topics:** 🚀 Production RAG Optimization, Cross-Encoder Reranking, Sub-15ms Semantic Caching, RAGAS Metrics, Binary Tree Codec DSA (LeetCode 297)
- **What I built:** Two-stage RAG pipeline, in-memory cosine semantic cache, Cross-Encoder reranker, and Java BFS Binary Tree Serializer.
- **Key insight:** Semantic caching cuts cloud inference costs by 35% by serving recurring queries without calling LLMs.

---

### Day 30
- **Topics:** 🏗️ GenAI System Design, Multi-Tenant Architecture, Dual Token Bucket Rate Limiting (RPM + TPM), Dynamic Model Routing, Search Autocomplete DSA (LeetCode 642)
- **What I built:** Multi-tenant gateway with Token Bucket quotas, intent-based dynamic model router, and Java Trie Search Autocomplete system.
- **Key insight:** Restricting both requests (RPM) and token volume (TPM) is mandatory to prevent tenant exhaustion.

---

### Day 31
- **Topics:** 🏆 GenAI Capstone + FAANG Interview Playbook, LFU Cache DSA (LeetCode 460)
- **What I built:** **Enterprise Autonomous Support Copilot** unifying all 8 architectural pillars, master 50-question FAANG interview guide, and O(1) Java LFU Cache.
- **Key insight:** Month 01 complete! Built full production-ready, observable, secure, and optimized GenAI infrastructure.

---

## 📊 Month 01 Final Summary (Days 01–31)
- **Days completed:** 31/31 (100% COMPLETE! 🏆)
- **Production Projects Built:** 25+
- **DSA Problems Solved (Java):** 40+ LeetCode Medium & Hard problems
- **Core Stacks Mastered:** Python (FastAPI, asyncio, Pydantic V2, LangChain, LangGraph), Java, PostgreSQL, ChromaDB, Redis, OpenTelemetry, Docker.

