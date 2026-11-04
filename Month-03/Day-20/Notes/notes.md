# Notes: Incremental Document Indexing & Content Hashing

## 1. Why Full Re-indexing is an Anti-Pattern
In production RAG systems with millions of documents:
- Documents undergo continuous incremental edits (e.g. fixing typos in a paragraph or adding an appendix).
- Dropping and recreating the vector index for every document update costs thousands of dollars in redundant embedding API calls and spikes latency.
- Incremental indexing breaks documents into deterministic chunks and computes SHA-256 hashes of each text payload.

## 2. Ingestion State Machine
```
For each incoming chunk C:
  hash = SHA256(C.text)
  if chunk_id in store:
    if store[chunk_id].hash == hash:
      -> NO-OP (Skip embedding calculation)
    else:
      -> UPDATE (Re-embed, overwrite vector, bump version)
  else:
    -> INSERT (Embed, register new vector)

For old chunks of Doc not in incoming set:
  -> DELETE (Purge stale vector from index)
```
