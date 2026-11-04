# Notes: Multi-Query Retrieval & Result Deduplication

## 1. Multi-Query Retrieval Paradigm
Users often formulate search queries narrowly or vaguely. Multi-query retrieval automatically diversifies queries into distinct semantic vectors:
1. **Facet Expansion**: Breaking a broad question into sub-components.
2. **Vocabulary Diversity**: Querying using formal technical terms vs practical implementation idioms.
3. **Perspective Synthesis**: Looking at architectural constraints vs coding patterns.

## 2. Result Deduplication & Provenance
When merging hits from $M$ sub-queries:
- **Deduplication by Chunk ID or Content Hash**: Avoids filling context windows with duplicate text passages.
- **Score Fusion**: Chunks returned across multiple queries receive higher confidence.
- **Provenance Tracking**: Each chunk records which specific generated query retrieved it, ensuring verifiable transparency.
