# Notes: Bi-Encoder vs Cross-Encoder Reranking

## 1. Architectural Differences
| Characteristic | Bi-Encoder (Dense Vector Search) | Cross-Encoder (Reranker) |
| :--- | :--- | :--- |
| **Input Format** | $E(q)$ and $E(d)$ processed separately | Concatenated $[CLS] + q + [SEP] + d$ |
| **Attention Mechanism** | Intra-query and intra-document only | Full all-to-all cross-attention across all tokens |
| **Pre-computation** | Document embeddings pre-computed & indexed | Cannot pre-compute (depends on specific query) |
| **Retrieval Speed** | $\sim 5$–$15$ ms (HNSW lookup) | $\sim 50$–$250$ ms for 20 candidates |
| **Retrieval Precision** | Moderate (compression to single fixed vector) | Very High (uncompressed pairwise cross-token interactions) |

## 2. Production Multi-Stage Pipeline
```mermaid
flowchart LR
    Q[User Query] --> BE[Bi-Encoder / BM25\nTop-50 Candidates]
    BE --> CE[Cross-Encoder Reranker\nFull Cross-Attention]
    CE --> Top[Top-5 Re-ordered Chunks]
    Top --> LLM[LLM Context Generator]
```
- **Stage 1 (High Recall)**: Cast a wide net (retrieve top 50–100 candidates) in $< 20$ ms.
- **Stage 2 (High Precision)**: Cross-encoder reranks only the top 50 candidates in $\sim 50$ ms.
