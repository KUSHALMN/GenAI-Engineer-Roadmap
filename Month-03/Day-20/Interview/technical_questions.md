# Interview Questions: Incremental Indexing & Tree Serialization

### Q1: How do you handle chunk boundary shifts when a single sentence is inserted at the top of a document?
**Answer**:
With fixed-size token chunking (e.g., 500-token chunks with 50-token overlap), inserting one sentence at the beginning changes the token boundaries of *every subsequent chunk* in the entire document, causing 100% of chunk hashes to change.
*Solutions*:
1. **Structure-Aware Chunking**: Chunk by Markdown headings, sections, or paragraph boundaries so edits within Section 1 don't alter the boundaries of Section 2.
2. **Content-Defined Chunking (Rabin-Karp / FastCDC)**: Uses rolling polynomial hashing to create boundaries at data-dependent fingerprint points, isolating insertions to local chunks.

### Q2: Why is a single pre-order traversal with null sentinels sufficient to reconstruct a binary tree?
**Answer**:
A standard pre-order traversal without null markers is ambiguous because multiple tree topologies can produce the same sequence of values (e.g. $[1, 2]$ could be left-child or right-child). By explicitly recording null pointers with a delimiter (e.g. `#`), the leaf terminations are unambiguously encoded, preserving the exact recursive structure without needing an in-order traversal array.

### Q3: How do you avoid O(N^2) string concatenation during tree serialization?
**Answer**:
Use `StringBuilder` in Java (or a list of string tokens in Python joined at the end via `",".join(tokens)`). Appending to a `StringBuilder` is $\mathcal{O}(1)$ amortized, keeping total serialization time strictly linear $\mathcal{O}(N)$ rather than $\mathcal{O}(N^2)$ caused by immutable string reallocations.
