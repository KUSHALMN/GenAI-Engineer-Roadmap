# 🧩 Java DSA — Day 22: Advanced Sliding Window Mastery

This module covers the core Sliding Window patterns used extensively in LeetCode Medium & Hard string and array problems.

---

## 📚 Problems & Complexity Analysis

| Problem | LeetCode | Difficulty | Time Complexity | Space Complexity | Key Pattern / Invariant |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Longest Substring Without Repeating Characters** | [LC 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | $\mathcal{O}(N)$ | $\mathcal{O}(\min(N, M))$ | Jump pointer with `lastSeen` index map or ASCII array |
| **Longest Repeating Character Replacement** | [LC 424](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Non-shrinking window with `(len - maxFreq) <= k` |
| **Minimum Window Substring** | [LC 76](https://leetcode.com/problems/minimum-window-substring/) | Hard | $\mathcal{O}(N + M)$ | $\mathcal{O}(M)$ | Two-pointer frequency map with `matchCount` match criteria |

---

## 💡 Sliding Window Architectural Templates

### 1. Dynamic Expanding & Shrinking Window (LC 3)
```java
int left = 0, maxLen = 0;
for (int right = 0; right < s.length(); right++) {
    char c = s.charAt(right);
    if (lastPos[c] != -1) {
        left = Math.max(left, lastPos[c] + 1); // Never move left backwards
    }
    lastPos[c] = right;
    maxLen = Math.max(maxLen, right - left + 1);
}
```

### 2. Frequency-Bounded Non-Shrinking Window (LC 424)
```java
int left = 0, maxFreq = 0;
for (int right = 0; right < s.length(); right++) {
    maxFreq = Math.max(maxFreq, ++count[s.charAt(right) - 'A']);
    if ((right - left + 1) - maxFreq > k) {
        count[s.charAt(left++) - 'A']--;
    }
}
return s.length() - left;
```

### 3. Target Frequency Matching Window (LC 76)
```java
int required = targetMap.size(), formed = 0;
// Expand right until formed == required
// Then shrink left while formed == required to find minimum window
```

---

## 🏃 Running Verification

```bash
javac Month-01/Day-22/DSA/*.java
java -cp Month-01/Day-22/DSA longest_substring
java -cp Month-01/Day-22/DSA character_replacement
java -cp Month-01/Day-22/DSA minimum_window_substring
```
