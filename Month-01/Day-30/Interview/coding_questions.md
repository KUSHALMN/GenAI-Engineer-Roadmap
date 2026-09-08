# 💻 Day 30 Coding Interview Questions: Search Autocomplete System

### Problem: Design Search Autocomplete System (LeetCode 642 - Hard / System Design DSA)
**Key Architecture (Trie with Top-K PriorityQueue)**:
1. Store sentences and their search frequencies in a Trie.
2. In each `TrieNode`, maintain a frequency table: `Map<String, Integer> counts`.
3. When the user types a character `c`:
   - Step down into `currNode.children[c]`.
   - If null, return empty list.
   - Use a bounded Min-Heap of size 3 to extract the 3 highest frequency sentences:
     - Comparator: sort primarily by frequency descending, break ties with ASCII alphabetical order.
4. When `#` is entered:
   - Commit the current accumulated string into the Trie, increment its count by 1, and reset search pointer to `root`.

**Complexity Analysis**:
- `input(c)`: Traversing 1 Trie edge takes $O(1)$. Extracting top 3 takes $O(L \log 3)$ where $L$ is the number of sentences sharing the prefix.
- Space Complexity: $O(\text{total characters across all indexed sentences})$.
