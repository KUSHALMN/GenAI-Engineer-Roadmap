"""
2D Dynamic Programming, Trie & Bit Manipulation Patterns (Python).
Problems Implemented:
1. 0/1 Knapsack Problem - O(N * W) time, O(N * W) or O(W) space
2. Longest Common Subsequence (LC 1143) - O(M * N) time, O(M * N) space
3. Trie (Prefix Tree) Implementation (LC 208) - O(L) time per word operation
4. Bit Manipulation: Single Number (LC 136) & Number of 1 Bits (LC 191)
"""

from typing import Dict, List, Optional


class DynamicProgramming2D:

    @staticmethod
    def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
        """Classic 0/1 Knapsack: maximize value within capacity."""
        n = len(weights)
        dp = [0] * (capacity + 1)

        for i in range(n):
            w = weights[i]
            v = values[i]
            # Traverse backwards to ensure 0/1 usage (each item used at most once)
            for cap in range(capacity, w - 1, -1):
                dp[cap] = max(dp[cap], dp[cap - w] + v)

        return dp[capacity]

    @staticmethod
    def longest_common_subsequence(text1: str, text2: str) -> int:
        """LC 1143: Longest Common Subsequence (2D DP table)."""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]


class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word = False


class Trie:
    """LC 208: Implement Trie (Prefix Tree)."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end_of_word = True

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return curr.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True


class BitManipulation:

    @staticmethod
    def single_number(nums: List[int]) -> int:
        """LC 136: Every element appears twice except for one. XOR property: x ^ x = 0."""
        res = 0
        for n in nums:
            res ^= n
        return res

    @staticmethod
    def hamming_weight(n: int) -> int:
        """LC 191: Number of 1 bits. Brian Kernighan's algorithm: n & (n - 1) flips lowest set bit."""
        count = 0
        while n > 0:
            n &= (n - 1)
            count += 1
        return count


if __name__ == "__main__":
    dp2 = DynamicProgramming2D()

    # 1. 0/1 Knapsack
    weights = [1, 2, 3]
    values = [60, 100, 120]
    cap = 5
    assert dp2.knapsack_01(weights, values, cap) == 220  # 100 + 120

    # 2. LCS LC 1143
    assert dp2.longest_common_subsequence("abcde", "ace") == 3
    assert dp2.longest_common_subsequence("abc", "abc") == 3
    assert dp2.longest_common_subsequence("abc", "def") == 0

    # 3. Trie LC 208
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.starts_with("app") is True
    trie.insert("app")
    assert trie.search("app") is True

    # 4. Bit Manipulation
    assert BitManipulation.single_number([4, 1, 2, 1, 2]) == 4
    assert BitManipulation.hamming_weight(11) == 3  # 11 = 1011_2

    print("All 2D DP, Trie, and Bit Manipulation Python tests passed successfully!")
