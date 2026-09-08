# 💻 Day 24 Coding Interview Questions: Word Break & Dynamic Programming

### Problem: Word Break (LeetCode 139 - Medium / High-Frequency FAANG)
**Key Insight**:
Let $dp[i]$ indicate whether the prefix $s[0 \dots i-1]$ can be segmented into words from `wordDict`.
For each index $i$ from 1 to $n$:
$$dp[i] = \bigvee_{j=\max(0, i-L)}^{i-1} (dp[j] \land (s[j \dots i] \in \text{dict}))$$
where $L$ is the length of the longest word in the dictionary.

**Complexity Analysis**:
- **Time Complexity**: Without optimization, checking all prefixes is $O(n^2 \cdot L)$. With max word length bounding ($L \ll n$), time becomes $O(n \cdot L^2)$.
- **Space Complexity**: $O(n)$ for the DP boolean array plus $O(W)$ for the dictionary HashSet.

**Trie Alternative**:
Traversing a Trie from index $i$ allows early termination as soon as a character path is missing, avoiding substring allocations in Java.
