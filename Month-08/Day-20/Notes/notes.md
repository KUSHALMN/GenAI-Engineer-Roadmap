# 📝 Notes — Day 20: Citation Audits & Fenwick Trees

- **Provenance Verification:** Claim extraction followed by NLI (Natural Language Inference) premise-hypothesis checking against cited chunks.
- **Fenwick 1-based Indexing:** BIT relies strictly on 1-based indices because `0 & (-0) = 0`, which creates an infinite loop.
- **BIT Space Complexity:** Exactly $O(N)$ auxiliary space compared to $4N$ for standard Segment Trees.
