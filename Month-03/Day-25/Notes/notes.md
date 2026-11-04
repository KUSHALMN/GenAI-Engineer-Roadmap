# Notes: Retrieval & Embedding Caching Invariants

## 1. Safe Cache Key Construction
Caching in production RAG systems saves significant embedding API costs and eliminates 80% of repeat retrieval latency. However, a naive cache keyed only on query text:
$$\text{Key} = \text{hash}(\text{query})$$
causes severe security and correctness vulnerabilities:
1. **Cross-Tenant Leakage**: Tenant B receives cached chunks originally retrieved by Tenant A.
2. **Stale Results on Corpus Updates**: If documents are added or updated, the old cached result continues to be returned.
3. **Filter Bypassing**: Query with filter `department=finance` returns cached results for `department=public`.

## 2. Canonical Cache Key Formula
$$\text{Key} = \text{SHA256}\Big(\text{normalized\_query} \;\|\; \text{tenant\_id} \;\|\; \text{model\_version} \;\|\; \text{index\_version} \;\|\; \text{sorted\_filters}\Big)$$
- Whenever a document is ingested, modified, or deleted, the `index_version` is bumped, rendering all existing keys obsolete without needing expensive full cache table scans.
