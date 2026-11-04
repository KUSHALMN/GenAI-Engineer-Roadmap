# Notes: Vector Search vs. Graph Retrieval Comparison

## 1. Trade-Off Comparison
| Evaluation Vector | Dense Vector Retrieval | Knowledge Graph Retrieval |
| :--- | :--- | :--- |
| **Strengths** | Fuzzy semantic match, unstructured text, fast cosine similarity | Explicit relational traversal, multi-hop joins, precise reasoning |
| **Weaknesses** | Fails at structural multi-hop entity chains, prone to semantic drift | Expensive upfront entity extraction, brittle schema constraints |
| **Storage Structure** | High-dimensional embedding vectors (HNSW / IVF) | Directed labeled property graphs (Nodes, Edges, Properties) |
| **Query Latency** | $< 10$ ms | $20$–$150$ ms (depending on recursive hop depth) |

## 2. Hybrid Graph-Vector Retrieval
The state-of-the-art architecture combines both:
1. **Entity Linking**: Identify seed entities in the user question.
2. **Graph Subgraph Expansion**: Traverse 1-to-2 hops in the knowledge graph to gather relational facts.
3. **Dense Vector Search**: Retrieve narrative evidence chunks filtered or boosted by the discovered entities.
4. **Joint Augmentation**: Pass both structured triples and unstructured text chunks to the LLM prompt.
