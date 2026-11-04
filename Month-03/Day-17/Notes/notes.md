# Notes: Multi-Hop RAG & Query Decomposition

## 1. The Multi-Hop Retrieval Challenge
Single-shot vector retrieval fails on multi-hop reasoning questions where the final answer requires combining facts from two or more unconnected documents:
- Query: *"Who is the CEO of the company that created the transformer model?"*
- Document A: States Google created transformers (mentions Google, transformers, no CEO).
- Document B: States Sundar Pichai is CEO of Google (mentions Sundar Pichai, CEO, Google, no transformers).
A single vector query cannot bridge the semantic gap because neither document independently contains both the question subject and the final answer.

## 2. Sequential Decomposition Pipeline
```mermaid
flowchart TD
    Q[Multi-Hop User Query] --> H1[Hop 1: Subquery 1\nIdentify Entity / Prerequisite]
    H1 --> D1[Retrieve Doc 1]
    D1 --> Fact[Extract Entity / Fact X]
    Fact --> H2[Hop 2: Conditioned Subquery 2\nFind Attribute of Fact X]
    H2 --> D2[Retrieve Doc 2]
    D2 --> Syn[Synthesize Final Cross-Document Answer]
```
- **Provenance Chaining**: The final answer links back to the entire DAG chain of source documents $[Doc_1 \to Doc_2]$.
