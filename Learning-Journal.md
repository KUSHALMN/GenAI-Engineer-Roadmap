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

---

## Month 02

### Day 01
- **Topics:** Advanced Agent Foundations, Multi-Tool Agent, Groq LLaMA 3, Coin Change DSA (Java)
- **What I built:** Agent with Search, Calculator, and Weather tools, and Java Coin Change DP.
- **Key insight:** ReAct pattern enables models to autonomously plan, execute tools, and synthesize results.

---

### Day 02
- **Topics:** FastAPI JWT Security, Docker Containerization, Climbing Stairs DSA (Java)
- **What I built:** Containerized JWT authentication microservice and O(1) space Climbing Stairs DP in Java.
- **Key insight:** Multi-stage Docker builds reduce image size and enhance container attack surface security.

---

### Day 03
- **Topics:** LangChain Tool Calling, Pydantic Schemas, House Robber DSA (Java)
- **What I built:** Native JSON schema tool calling agent with AST-safe expression eval and House Robber I & II DP in Java.
- **Key insight:** Native tool schemas eliminate regex parsing fragility inherent in naive text-based agent loops.

---

### Day 04
- **Topics:** LLM Caching, Deterministic Hashing, TTL Cache, LRU Cache from scratch (Python & Java)
- **What I built:** In-memory LLM response cache with SHA-256 key normalization, savings telemetry, and LeetCode 146 LRU Cache from scratch.
- **Key insight:** Deterministic key canonicalization (whitespace strip, sorted JSON keys) is crucial to avoid spurious cache misses.

---

### Day 05
- **Topics:** LLM Evaluation, RAG Triad, Pairwise LLM-as-a-Judge, Two Pointers DSA (Python & Java)
- **What I built:** Golden evaluation dataset, rule-based token F1 evaluator, RAG Triad (faithfulness/groundedness), and position-bias mitigated LLM Judge.
- **Key insight:** Swapping candidate presentation order ($A \text{ vs } B$ and $B \text{ vs } A$) is mandatory to eliminate position bias.

---

### Day 06
- **Topics:** LLM Observability, Structured JSON Logging, Latency Tracking (TTFT/ITL), Sliding Window DSA (Python & Java)
- **What I built:** JSON logging with contextvars trace propagation, fine-grained span tracker, and Sliding Window algorithms (LC 3, 209, 643).
- **Key insight:** Tracking Time To First Token (TTFT) and Inter-Token Latency (ITL) separates compute-bound prefill from memory-bound decoding.

---

### Day 07
- **Topics:** Production Reliability, Exponential Backoff, Rate Limiting, Monotonic Stack DSA (Python & Java)
- **What I built:** Exponential backoff with full jitter, thread-safe Token Bucket rate limiter, multi-provider fallback client, and Daily Temperatures (LC 739).
- **Key insight:** Full jitter prevents thundering herd synchronization during upstream provider recovery.

---

### Day 08
- **Topics:** GenAI Security, Prompt Injection Testing, Tool Permissions, Binary Search DSA (Python & Java)
- **What I built:** Automated injection test runner, XML delimiter framing, RBAC tool permissions, secret output scanner, and Rotated Binary Search (LC 33).
- **Key insight:** Defense-in-depth requires isolating context via strict XML frames and enforcing least-privilege tool execution.

---

### Day 09
- **Topics:** Guardrails, PII Masking, HITL Tool Approvals, Linked List DSA (Python & Java)
- **What I built:** Input guardrail policy engine, reversible PII pseudonymization, Human-in-the-Loop tool approvals, and Linked List operations.
- **Key insight:** Reversible pseudonymization enables sending sanitized text to public models while restoring true entities locally.

---

### Day 10
- **Topics:** Structured Outputs, Pydantic Reflection Retry, Tool Calling, Binary Tree Traversals (Python & Java)
- **What I built:** Pydantic response models, reflection retry on validation failure, safe tool dispatcher, and Tree BFS/DFS (LC 102, 104, 226).
- **Key insight:** Feeding exact Pydantic ValidationError text back into model prompts enables reliable self-correction.

---

### Day 11
- **Topics:** Agent Architectures, ReAct Loop, Workflows vs Agents, BST Operations (Python & Java)
- **What I built:** Deterministic sequential workflow, intent router, ReAct agent loop with max iteration bounds, and BST operations (LC 700, 701, 450, 98, 235).
- **Key insight:** Use deterministic DAGs for strict latency/cost SLAs and reserve autonomous agents for open-ended research.

---

### Day 12
- **Topics:** Model Context Protocol (MCP), JSON-RPC 2.0, Tool Discovery, Heaps DSA (Python & Java)
- **What I built:** Minimal MCP tool server exposing telemetry and calculator, discovery client, and Priority Queue patterns (LC 215, 347, 23).
- **Key insight:** Standardized JSON-RPC tool contracts decouple agent brains from tool execution environments.

---

### Day 13
- **Topics:** Context Engineering, Hierarchical Auto-Summarization, Episodic Memory, Intervals DSA (Python & Java)
- **What I built:** Conversation buffer, auto-summarization of older turns, long-term memory store with Last-Write-Wins, and Merge Intervals (LC 56, 57, 253).
- **Key insight:** Hierarchical memory compression preserves critical context while enforcing strict token budget ceilings.

---

### Day 14
- **Topics:** Advanced RAG, HyDE, Hybrid Search (BM25 + Dense RRF), Cross-Encoder Reranking, Graph BFS/DFS (Python & Java)
- **What I built:** HyDE query rewriter, Reciprocal Rank Fusion hybrid retriever, contextual reranker, and Graph algorithms (LC 200, 207).
- **Key insight:** Reciprocal Rank Fusion combines the precision of keyword search with the conceptual recall of dense embeddings.

---

### Day 15
- **Topics:** Multimodal GenAI, Document OCR Layouts, Vision Prompts, Topological Sort (Python & Java)
- **What I built:** OCR text & bounding box extractor, multimodal prompt flow, image token estimator, and Topological Sort (LC 210).
- **Key insight:** 512x512 tile patching dictates vision model token pricing; downscaling high-res documents saves thousands in API costs.

---

### Day 16
- **Topics:** GenAI Data Engineering, JSONL Validation, Deduplication, Disjoint Set Union (Python & Java)
- **What I built:** Text cleaning pipeline, JSONL validator, exact SHA-256 + fuzzy Jaccard deduplication, and Union-Find (LC 547, 684).
- **Key insight:** High-quality deduplication and filtering directly improve fine-tuning convergence speed and eliminate regurgitation.

---

### Day 17
- **Topics:** Advanced Inference Optimization, Continuous Batching, KV Cache Sizing, Backtracking DSA (Python & Java)
- **What I built:** Latency tracker, streaming TTFT benchmark, dynamic batching simulator, and Backtracking algorithms (LC 78, 46, 51).
- **Key insight:** Autoregressive decoding is memory-bandwidth bound; PagedAttention and GQA eliminate KV cache memory fragmentation.

---

### Day 18
- **Topics:** Model Routing & Adaptation, Fallback Chains, 1D Dynamic Programming (Python & Java)
- **What I built:** Small vs Large model complexity router, multi-provider fallback router, adaptation decision matrix, and 1D DP (LC 70, 198, 322).
- **Key insight:** Routing 60% of simple tasks to 8B models cuts inference costs by 50% while maintaining frontier intelligence for complex queries.

---

### Day 19
- **Topics:** GenAI System Design, LLMOps, Architecture Diagrams, SLOs, 2D DP & Trie (Python & Java)
- **What I built:** Production RAG and Agent system design specifications, Draw.io architecture diagram, quantitative SLIs/SLOs, and 2D DP (Knapsack, LC 1143, LC 208).
- **Key insight:** Production architectures require clear defense-in-depth: API gateway, semantic caching, guardrails, and model fallbacks.

---

### Day 20
- **Topics:** FAANG GenAI Interview Playbook, Production Capstone Service, Java DSA Masterclass
- **What I built:** Enterprise FastAPI Capstone service with Auth, Caching, RAG, and Security, Dockerfile, FAANG interview Q&A, and Java DSA Masterclass.
- **Key insight:** Month 02 Days 04 to 20 complete! Fully prepared for Staff/Senior GenAI Engineer production systems and technical interviews.



---

## Month 02 — New Entries (Days 01–03)

### Day 32 (Month 02 - Day 01)
- **Topics:** LLM Fine-Tuning + LoRA/PEFT, Dataset Preparation, Training Loop, BLEU/F1 Evaluation, Coin Change DP (LC 322)
- **What I built:** Full fine-tuning pipeline — `prepare_dataset.py` (Alpaca-format JSONL), `train.py` (LoRA loop), `evaluate.py` (BLEU-1, Keyword F1, Exact Match), and Java Coin Change bottom-up DP.
- **Key insight:** LoRA trains only ~0.06% of model parameters by injecting low-rank matrices `ΔW = BA` — 10-100x memory savings vs full fine-tuning with minimal quality loss.
- **DSA insight:** Coin Change = unbounded knapsack DP. Greedy fails on non-canonical coin sets — always use `dp[i] = min(dp[i-coin]+1)`.

---

### Day 33 (Month 02 - Day 02)
- **Topics:** Docker + JWT Authentication, FastAPI OAuth2, Bcrypt, Token Expiry, Climbing Stairs DP (LC 70)
- **What I built:** Production FastAPI JWT auth service with `/auth/token`, `/me`, `/protected` endpoints, Dockerfile, docker-compose, 8 unit tests, and Java Climbing Stairs O(1) space DP.
- **Key insight:** Always pass `algorithms=["HS256"]` explicitly to `jwt.decode()` — prevents the `alg: none` attack where attacker strips signature verification.
- **DSA insight:** Climbing Stairs = Fibonacci DP. `dp[i] = dp[i-1] + dp[i-2]`. Space-optimize to two variables. Generalizes to k-steps with inner loop.

---

### Day 34 (Month 02 - Day 03)
- **Topics:** LangChain Tool-Calling Agents, ReAct Pattern, Safe AST Eval, Pydantic Tool Schemas, House Robber DP (LC 198 + 213)
- **What I built:** LangChain agent with 3 tools (Search, Calculator with safe AST eval, Weather), FastAPI endpoint, 9 unit tests, benchmark analysis, and Java House Robber I + II O(1) space DP.
- **Key insight:** Native JSON schema tool calling (LangChain `create_tool_calling_agent`) is far more reliable than text-based ReAct parsing — no regex fragility, structured tool inputs enforced by Pydantic.
- **DSA insight:** House Robber II (circular) = run linear robber twice on `[0, n-2]` and `[1, n-1]`, take max. Breaking the circle by excluding one endpoint reduces it to the linear problem.

---

### Day 21 (Month 02)
- **Topics:** Enterprise LLM Evaluation Service, Lexical Metrics, Groq LLM-as-a-Judge, Two Pointers (LC 167, 15, 11)
- **What I built:** FastAPI evaluation microservice with Exact Match, Normalized EM, Token F1, LLM Judge fallback, and Java Two Pointers suite.

---

### Day 22 (Month 02)
- **Topics:** Advanced RAG Triad Evaluator, Hallucination Detection, Sliding Window (LC 3, 209, 438)
- **What I built:** Context Relevance, Faithfulness, and Answer Relevance triad scoring pipeline with sentence-level hallucination detection, and Java Sliding Window suite.

---

### Day 23 (Month 02)
- **Topics:** Corrective RAG (CRAG), Self-RAG Guardrails, LRU Cache (LC 146)
- **What I built:** Document grading evaluator (CORRECT, AMBIGUOUS, INCORRECT), knowledge striping, Self-RAG critique reflection tokens, and Java LRU Cache O(1).

---

### Day 24 (Month 02)
- **Topics:** GenAI Observability & Distributed Tracing, Token Economics, Monotonic Queue/Stack (LC 239, 739, 496)
- **What I built:** ContextVars request ID propagation, structured JSON logger, latency breakdown checkpoints, cost tracker per model, and Java Monotonic Deque for Sliding Window Maximum O(N).

---

### Day 25 (Month 02)
- **Topics:** Production Reliability & Async LLM, Exponential Backoff with Full Jitter, Circuit Breakers, Advanced Binary Search (LC 33, 153, 1011)
- **What I built:** Resilient async client, token bucket rate limiter, three-state circuit breaker, fallback cascading router, and Java Binary Search on answer space O(N log(sum-max)).

---

### Day 26 (Month 02)
- **Topics:** GenAI Security & Threat Defense, Prompt Injection Firewall, PII Masker, Fast/Slow Pointers (LC 141, 142, 234)
- **What I built:** Multi-vector injection detector, unicode zero-width character scrubber, token limit DoS guard, strict tool execution allowlist, and Java Floyd's cycle detection.

---

### Day 27 (Month 02)
- **Topics:** Guardrails & Safe AI Execution, Input/Output Gateways, HITL Policies, Advanced Binary Trees (LC 543, 124, 297)
- **What I built:** Input/output safety guardrail pipelines, JSON schema validator, severity-based PII detector, Human-in-the-Loop tool confirmation gate, and Java Tree Codec (LC 297).

---

### Day 28 (Month 02)
- **Topics:** Structured Output & Tool Calling Engine, Pydantic Models, JSON Repair, Trie Autocomplete (LC 208, 211, 14)
- **What I built:** Pydantic dataclass models, regex JSON cleaner & fence stripper, tool dispatcher registry, and Java Trie with wildcard '.' search.

---

### Day 29 (Month 02)
- **Topics:** Autonomous ReAct Agents & State Workflows, Dynamic Tool Selection, Advanced Heap (LC 23, 347, 295)
- **What I built:** Autonomous ReAct reasoning loop, state schema with step budgets, intent router, semantic tool filter, and Java Dual-Heap Median Finder O(1).

---

### Day 30 (Month 02)
- **Topics:** Model Context Protocol (MCP) Architecture, JSON-RPC 2.0, Graph Shortest Path (LC 743, 787)
- **What I built:** Full MCP Server and Client implementing `tools/list`, `tools/call`, `resources/list`, `resources/read`, and Java Dijkstra O(E log V) & Bellman-Ford O(K*E).

---

## Month 03 — Advanced AI Engineering & Systems

### Day 01 (Month 03)
- **Topics:** Context Engineering & Multi-Tier Memory, Token Budgets, Disjoint Set Union (LC 547, 684, 1584)
- **What I built:** Token budget partition manager, sliding window conversation memory, abstractive progressive summarizer, episodic key-value memory store, and Java DSU with Kruskal's MST O(E log E).

---

### Day 02 (Month 03)
- **Topics:** Advanced Multi-Stage RAG Funnel, BM25, RRF Hybrid Search, HyDE, Reranker, Advanced Backtracking (LC 51, 79, 46)
- **What I built:** Okapi BM25 sparse index, Reciprocal Rank Fusion (RRF), HyDE hypothetical doc expander, cross-encoder reranker, parent-child hierarchical chunker, and Java N-Queens O(N!).

---

### Day 03 (Month 03)
- **Topics:** Multimodal GenAI Systems & Document Pipelines, OCR, Whisper ASR, TTS, Vision QA, Tree DP & Knapsack (LC 337, 416, 322)
- **What I built:** Multi-format document parser, receipt OCR pipeline, CLIP image embeddings, audio speech transcriber, TTS synthesizer, Vision-Language Image QA, Multimodal RAG, and Java House Robber III Tree DP O(N).

---

## 📊 Milestone Summary
- **Total Days Completed:** 64 Days across Month 01, Month 02, and Month 03.
- **Month 01 Status:** 100% Completed ✅
- **Month 02 Status:** 100% Completed ✅
- **Month 03 Status:** Active & Expanding 🚀

