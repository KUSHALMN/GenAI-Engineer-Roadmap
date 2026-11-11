# 📝 Notes — Day 19: Uncertainty Abstention & Tries

- **Semantic Entropy:** Distinct from lexical entropy; multiple paraphrases expressing the same semantic claim must be merged into one cluster.
- **XOR Properties:** $x \oplus x = 0$ and $x \oplus 0 = x$. Associative and commutative, isolating the unique non-paired element in $O(N)$ time and $O(1)$ space.
- **Trie Traversal:** Store `TrieNode[] children = new TrieNode[26]` for direct $O(1)$ indexing by `c - 'a'`.
