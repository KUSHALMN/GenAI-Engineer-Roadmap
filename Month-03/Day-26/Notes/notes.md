# Notes: Retrieval Evaluation Dataset Governance

## 1. Principles of a Golden Retrieval Benchmark
Evaluating RAG systems requires fixed, reproducible benchmark datasets with verifiable ground-truth chunk labels:
1. **Difficulty Stratification**:
   - *Easy*: Direct lexical match (e.g., standard definitions).
   - *Medium*: Requires synonym resolution or paragraph synthesis.
   - *Hard*: Requires multi-hop joins across disparate documents.
   - *Unanswerable (Negative Controls)*: Queries whose answers do NOT exist in the corpus (tests hallucination rate and proper abstention).

## 2. Dataset Schema (JSONL)
```json
{
  "query_id": "q001",
  "query": "string",
  "difficulty": "easy | medium | hard | unanswerable",
  "expected_chunk_ids": ["ch_01", "ch_02"],
  "expected_facts": ["ground_truth_claim_1"],
  "is_answerable": true
}
```
Automated continuous validation prevents merged PRs from breaking the golden test set.
