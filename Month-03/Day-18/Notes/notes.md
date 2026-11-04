# Notes: GraphRAG Foundations & Knowledge Graphs

## 1. What is GraphRAG?
GraphRAG (Microsoft Research, 2024) combines structured Knowledge Graphs with unstructured text chunk indexing to enable global dataset comprehension:
- **Vector Search Weakness**: Excels at local factual lookups ("What is X's phone number?"), but completely fails at holistic/global questions ("What are the main organizational themes across these 5,000 documents?").
- **Graph Construction**: Extracts entities (Nodes) and typed relationships (Edges), then performs entity resolution to link synonyms.
- **Hierarchical Leiden Clustering**: Groups related nodes into communities and generates recursive executive summaries.

## 2. Key Primitives
1. **Entity Extraction**: Identifying named entities and assigning ontologies (`Person`, `Organization`, `Concept`).
2. **Entity Canonicalization**: Mapping variations (`"Google Inc"`, `"Google LLC"`, `"Alphabet"`) to a single canonical entity.
3. **Relationship Triples**: $(Subject, Predicate, Object)$ with evidence text spans.
