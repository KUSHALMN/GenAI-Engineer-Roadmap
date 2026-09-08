# 💼 Day 30 Recruiter & System Architecture Interview Questions

### 1. "How do you approach designing an enterprise GenAI platform from scratch?"
**Talking Points**:
- "I divide the architecture into four core pillars:
  1. **Ingress & Protection**: Centralized API Gateway handling authentication, dual Token Bucket rate limiting (RPM + TPM), and fast input guardrails.
  2. **Cost & Latency Optimization**: A semantic cache cluster paired with an intelligent model router that partitions traffic between cost-efficient open-source models and frontier reasoning models.
  3. **Data & Retrieval**: Two-stage RAG with hybrid search and Cross-Encoder reranking backed by asynchronous CDC pipelines.
  4. **Observability & Governance**: Distributed OpenTelemetry tracing logging real-time unit economics, token burn, and $p95$ latency."

### 2. "What is your philosophy on self-hosting open-weight models (vLLM) vs. using proprietary APIs (OpenAI/Anthropic)?"
**Talking Points**:
- "It is rarely an all-or-nothing decision.
- We self-host open models (e.g. LLaMA-3.3 70B on vLLM with PagedAttention) for high-volume, latency-sensitive tasks like classification, embedding generation, reranking, and internal compliance where data cannot leave our VPC.
- We reserve proprietary frontier APIs for high-reasoning tasks, complex code generation, or multi-modal synthesis where frontier capabilities justify the premium pricing."
