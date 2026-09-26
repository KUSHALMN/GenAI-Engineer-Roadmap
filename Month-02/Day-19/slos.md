# 🎯 Service Level Objectives (SLOs) & Indicators (SLIs) for GenAI

## 1. Latency & Responsiveness

| Indicator (SLI) | Target Objective (SLO) | Measurement Window | Alert Threshold |
|---|---|---|---|
| **Time To First Token (TTFT)** | $P_{95} \le 800\text{ ms}$ (streaming) | Rolling 1 hour | $> 1200\text{ ms}$ for 5 mins |
| **End-to-End Latency (P95)** | $P_{95} \le 2.5\text{ s}$ (RAG completed) | Rolling 1 hour | $> 3.5\text{ s}$ for 5 mins |
| **Inter-Token Latency (ITL)** | $P_{95} \le 25\text{ ms}$ per token | Rolling 1 hour | $> 40\text{ ms}$ for 5 mins |

---

## 2. Reliability & Availability

| Indicator (SLI) | Target Objective (SLO) | Measurement Window | Alert Threshold |
|---|---|---|---|
| **Service Availability** | $\ge 99.9\%$ successful HTTP 200 responses | Monthly rolling | Error rate $> 1.0\%$ over 2 mins |
| **Provider Fallback Rate** | $\le 2.0\%$ of requests trigger secondary fallback | Daily | $> 5.0\%$ over 15 mins |
| **Circuit Breaker Status** | Zero active trip events lasting $> 2\text{ minutes}$ | Real-time | Any trip lasting $> 60\text{ s}$ |

---

## 3. Data Quality, RAG & Hallucination

| Indicator (SLI) | Target Objective (SLO) | Measurement Window | Alert Threshold |
|---|---|---|---|
| **RAG Faithfulness / Groundedness** | $\ge 98.0\%$ factual attribution | Weekly audit sample | $< 95.0\%$ |
| **Retrieval Context Recall@5** | $\ge 90.0\%$ relevant chunk coverage | Weekly benchmark | $< 85.0\%$ |
| **Cache Hit Rate** | $\ge 35.0\%$ (Exact + Semantic) | Daily rolling | $< 25.0\%$ |

---

## 4. Cost & Token Governance

| Indicator (SLI) | Target Objective (SLO) | Measurement Window | Alert Threshold |
|---|---|---|---|
| **Cost Per 1K Queries** | $\le \$2.50$ blended cost | Daily | $> \$3.50$ daily average |
| **Max Token Ceiling per Request** | $100\%$ requests strictly capped at $8,192$ tokens | Per request | Any request exceeding limit |
