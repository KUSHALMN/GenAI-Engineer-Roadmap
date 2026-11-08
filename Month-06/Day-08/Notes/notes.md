# Engineering Notes — Day 08: Multimodal RAG & Prefix Sum Mechanics

## 1. Multimodal Evidence Packaging
- Text chunks $\rightarrow$ Markdown formatted strings.
- Tables $\rightarrow$ Clean markdown / JSON matrix representation.
- Image crops $\rightarrow$ Low-resolution base64 thumbnails or visual tokens.

## 2. Prefix Sum Complexity
- $O(N)$ single pass, $O(N)$ hashmap auxiliary space.
- Base condition `prefixMap.put(0, 1)` accounts for valid subarrays starting at index 0.
