# 🌟 FAANG Behavioral Interview Stories (STAR Method)

## Story 1: Resolving a Production Latency & Cost Crisis (Runaway LLM Spend)
- **Situation**: Following the launch of an autonomous agent feature, monthly LLM API bills surged by 340%, and P95 latency degraded to 8.2 seconds due to unconstrained agent loops and duplicate queries.
- **Task**: As the Lead GenAI Engineer, I was tasked with reducing costs by $>50\%$ and bringing P95 latency under 2 seconds without impacting answer quality.
- **Action**:
  1. Built an in-memory and Redis exact-match cache with deterministic SHA-256 parameter hashing, caching $38\%$ of repetitive user questions with $<5\text{ms}$ return time.
  2. Implemented hard agent loop safety controls: capped iterations at 5 steps and introduced a strict token budget guardrail.
  3. Replaced large frontier model calls for simple classification tasks with an 8B parameter model via a rule-based model router.
- **Result**: Reduced monthly token expenditure by $62\%$ (\$42,000/month savings) and dropped P95 latency from 8.2s to 1.4s, exceeding company SLOs.

---

## Story 2: Technical Disagreement on Fine-Tuning vs RAG Architecture
- **Situation**: Our product leadership wanted to fine-tune an open-source 70B model on internal company customer support documentation to eliminate the need for a search database.
- **Task**: I needed to demonstrate why fine-tuning alone would not solve hallucination and stale knowledge issues, and persuade the team to adopt a Hybrid RAG architecture instead.
- **Action**:
  1. Developed a fast prototype comparing a fine-tuned LoRA model against a hybrid RAG pipeline (BM25 + Dense vector search + Cross-Encoder reranker).
  2. Created a golden evaluation dataset (`JSONL`) measuring Faithfulness and Context Relevance.
  3. Showed that the fine-tuned model hallucinated outdated return policies 23% of the time, while the RAG pipeline achieved 98.4% groundedness with verifiable inline citations.
- **Result**: The team unanimously agreed to adopt the Hybrid RAG architecture. Document updates now take effect in real-time with zero training cost.

---

## Story 3: Navigating a Severe GenAI Security Vulnerability
- **Situation**: Security audit discovered that our agent could be manipulated via indirect prompt injection hidden inside customer-submitted PDF documents, leading to potential data exfiltration.
- **Task**: Secure the agent execution environment against injection attacks before the enterprise release.
- **Action**:
  1. Implemented a dual-boundary defense: wrapped all retrieved context in strictly isolated XML tags and added system prompt instructions explicitly forbidding command execution from context.
  2. Developed a pre-execution tool authorization policy engine (RBAC) that blocks shell execution and path traversal attempts.
  3. Created an automated security test suite with 50+ injection attack vectors to continuously gate CI/CD merges.
- **Result**: Neutralized all injection attack vectors, passed SOC2 Type II compliance audit, and successfully launched to Fortune 500 enterprise customers.
