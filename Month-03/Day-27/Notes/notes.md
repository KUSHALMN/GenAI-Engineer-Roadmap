# Notes: Information Retrieval (IR) Evaluation Metrics

## 1. Metric Hierarchy in Production RAG
| Metric | Purpose | When to Use |
| :--- | :--- | :--- |
| **Recall@K** | Fraction of relevant documents retrieved in Top-$K$. | Baseline coverage check. In RAG, high Recall@K is mandatory because downstream LLMs cannot cite what was never retrieved. |
| **Precision@K** | Fraction of retrieved items that are relevant. | Evaluates noise injection and context window pollution. |
| **MRR (Mean Reciprocal Rank)** | Position of the *first* relevant chunk ($1/rank$). | Best for factual single-hop queries where one good chunk suffices. |
| **MAP (Mean Average Precision)** | Area under precision-recall curve across multiple relevant chunks. | Best for queries requiring multi-chunk synthesis. |
| **NDCG@K** | Discounted Cumulative Gain normalized against ideal ranking. | Best when chunks have graded relevance (Highly relevant = 3, Marginally = 1, Irrelevant = 0). |

## 2. Invariant
Retrieval metrics evaluate the **retrieval stage in isolation** (pre-LLM), preventing LLM generation variance from obscuring search pipeline regressions.
