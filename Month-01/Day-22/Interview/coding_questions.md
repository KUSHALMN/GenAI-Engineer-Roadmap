# 💻 Day 22 - Coding Interview Preparation: Sliding Window & Two Pointers

---

### Problem 1: Longest Substring Without Repeating Characters (LeetCode 3 - Medium)
- **Problem Statement**: Given a string `s`, find the length of the longest substring without duplicate characters.
- **Core Pattern**: Variable-size Sliding Window with HashMap / ASCII Index lookup.
- **Key Insight**: Maintain the last seen index of each character. When a duplicate `s[right]` is encountered at index `prev`, update `left = max(left, prev + 1)`.
- **Complexity**:
  - Time: $O(N)$ (single pass)
  - Space: $O(\min(N, \Sigma))$ where $\Sigma$ is character set size ($O(1)$ for ASCII).

```java
public int lengthOfLongestSubstring(String s) {
    int[] last = new int[128];
    Arrays.fill(last, -1);
    int maxLen = 0, left = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (last[c] >= left) {
            left = last[c] + 1;
        }
        last[c] = right;
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

---

### Problem 2: Longest Repeating Character Replacement (LeetCode 424 - Medium)
- **Problem Statement**: Given string `s` and integer `k`, find the max length of a substring with identical characters after performing at most `k` character replacements.
- **Invariant**: `(window_size - max_frequency) <= k` must hold for a valid window.
- **Optimization**: The window does not need to shrink! It only slides forward if invalid, preserving maximum valid size achieved so far.
- **Complexity**:
  - Time: $O(N)$
  - Space: $O(26) = O(1)$

```java
public int characterReplacement(String s, int k) {
    int[] count = new int[26];
    int maxFreq = 0, left = 0, right = 0;
    for (; right < s.length(); right++) {
        maxFreq = Math.max(maxFreq, ++count[s.charAt(right) - 'A']);
        if ((right - left + 1) - maxFreq > k) {
            count[s.charAt(left++) - 'A']--;
        }
    }
    return right - left;
}
```

---

### Problem 3: Minimum Window Substring (LeetCode 76 - Hard)
- **Problem Statement**: Given strings `s` and `t`, return the minimum window in `s` that contains all characters of `t` (including duplicates).
- **Core Pattern**: Two-pointer Sliding Window with `have` vs `need` frequency matching.
- **Algorithm**:
  1. Count character frequencies of `t` in `need[128]`. Count distinct characters as `uniqueNeeded`.
  2. Expand `right`: Add `s[right]` to `window[128]`. If `window[c] == need[c]`, increment `matched`.
  3. While `matched == uniqueNeeded`: record minimum window, remove `s[left]` and increment `left`.
- **Complexity**:
  - Time: $O(|S| + |T|)$
  - Space: $O(1)$ (fixed 128 integer arrays).
