# 📊 LLM Evaluation & Testing Report

## 1. Overview
This benchmark evaluates LLM generations using a hybrid multi-layer framework:
1. **Deterministic Rule-Based Filters**: Exact match, Keyword coverage, Token-level Precision/Recall/F1.
2. **RAG Triad Assessment**: Context Relevance, Faithfulness (groundedness / hallucination rate), Answer Relevance.
3. **Pairwise LLM-as-a-Judge**: Model A vs Model B with position-bias counter-swapping.

---

## 2. Evaluation Results Summary

| Sample ID | Query Category | Rule-Based F1 | Groundedness | Answer Relevance | Pairwise Winner |
|---|---|---|---|---|---|
| `eval_001` | Architecture (Attention) | 0.88 | 1.00 (High) | 0.92 | Version A (Concise) |
| `eval_002` | Fine-Tuning (LoRA) | 0.82 | 0.95 (High) | 0.89 | Version A (Accurate) |
| `eval_003` | Context (Lost in Middle) | 0.79 | 0.90 (High) | 0.85 | Tie |
| `eval_004` | Retrieval (Sparse vs Dense) | 0.91 | 1.00 (High) | 0.95 | Version A |
| `eval_005` | Sampling (Greedy temp=0) | 0.85 | 1.00 (High) | 0.90 | Version A |

---

## 3. Position Bias & LLM Judge Findings

- **Order Sensitivity**: Without input swapping, LLM judges exhibit a 15–20% bias toward the first presented candidate (`Candidate 1`).
- **Mitigation**: Running symmetric passes ($A \text{ vs } B$ and $B \text{ vs } A$) eliminates position bias and classifies ambiguous cases as explicit ties.
- **Hallucination Detection**: Sentence-level n-gram overlap between answer and reference context effectively flags ungrounded facts with low latency.
