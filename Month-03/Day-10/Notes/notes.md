# Notes: Conversational Query Rewriting & Anaphora Resolution

## 1. Why Query Rewriting is Mandatory in Multi-Turn RAG
In conversational RAG, users naturally refer to previous context using pronouns and implicit references:
- User Turn 1: "What is Apache Lucene?"
- Assistant Turn 1: "Apache Lucene is a high-performance, full-featured text search engine library written entirely in Java."
- User Turn 2: "How does it compare to Elasticsearch?"
If User Turn 2 is sent directly to the vector database or BM25, the pronoun **"it"** will lack semantic association with "Apache Lucene", resulting in retrieval of irrelevant documents.

## 2. Core Rewriting Techniques
1. **Coreference / Anaphora Resolution**:
   - Replaces pronouns (`it`, `they`, `its`, `this`) with concrete antecedent nouns extracted from conversational memory.
2. **Domain Term & Acronym Expansion**:
   - Expands abbreviations like `k8s` to `kubernetes` and `rag` to `retrieval augmented generation` to improve BM25 recall.
3. **Conversational De-noising**:
   - Strips polite introductory filler ("Can you tell me", "I was wondering if") which adds noise tokens to dense embeddings.
