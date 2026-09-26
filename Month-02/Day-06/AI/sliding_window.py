"""
Sliding Window DSA Pattern (Python).
Problems Implemented:
1. Longest Substring Without Repeating Characters (LC 3) - O(N) time, O(min(m, n)) space
2. Minimum Size Subarray Sum (LC 209) - O(N) time, O(1) space
3. Maximum Average Subarray I (LC 643) - Fixed size window O(N) time, O(1) space
4. Minimum Window Substring (LC 76) - Dynamic size window O(N + M) time
"""

from typing import Dict, List


class SlidingWindow:

    @staticmethod
    def length_of_longest_substring(s: str) -> int:
        """
        LC 3: Longest Substring Without Repeating Characters.
        Dynamic sliding window using hash map to store last seen index.
        """
        char_index: Dict[str, int] = {}
        left = 0
        max_length = 0

        for right, ch in enumerate(s):
            if ch in char_index and char_index[ch] >= left:
                left = char_index[ch] + 1
            char_index[ch] = right
            max_length = max(max_length, right - left + 1)

        return max_length

    @staticmethod
    def min_sub_array_len(target: int, nums: List[int]) -> int:
        """
        LC 209: Minimum Size Subarray Sum.
        Find minimal length of contiguous subarray of which sum >= target.
        """
        left = 0
        current_sum = 0
        min_len = float("inf")

        for right in range(len(nums)):
            current_sum += nums[right]

            while current_sum >= target:
                min_len = min(min_len, right - left + 1)
                current_sum -= nums[left]
                left += 1

        return int(min_len) if min_len != float("inf") else 0

    @staticmethod
    def find_max_average(nums: List[int], k: int) -> float:
        """
        LC 643: Maximum Average Subarray I.
        Fixed-size sliding window of length k.
        """
        window_sum = sum(nums[:k])
        max_sum = window_sum

        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            max_sum = max(max_sum, window_sum)

        return max_sum / k

    @staticmethod
    def min_window(s: str, t: str) -> str:
        """
        LC 76: Minimum Window Substring.
        Find smallest substring in s that contains all chars of t.
        """
        if not s or not t:
            return ""

        target_counts: Dict[str, int] = {}
        for char in t:
            target_counts[char] = target_counts.get(char, 0) + 1

        window_counts: Dict[str, int] = {}
        required = len(target_counts)
        formed = 0

        left = 0
        ans = (float("inf"), None, None)  # (window_len, left, right)

        for right, char in enumerate(s):
            window_counts[char] = window_counts.get(char, 0) + 1

            if char in target_counts and window_counts[char] == target_counts[char]:
                formed += 1

            while left <= right and formed == required:
                # Try to shrink window from left
                if (right - left + 1) < ans[0]:
                    ans = (right - left + 1, left, right)

                left_char = s[left]
                window_counts[left_char] -= 1
                if left_char in target_counts and window_counts[left_char] < target_counts[left_char]:
                    formed -= 1
                left += 1

        return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]


if __name__ == "__main__":
    sw = SlidingWindow()

    # Test LC 3
    assert sw.length_of_longest_substring("abcabcbb") == 3
    assert sw.length_of_longest_substring("bbbbb") == 1
    assert sw.length_of_longest_substring("pwwkew") == 3

    # Test LC 209
    assert sw.min_sub_array_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert sw.min_sub_array_len(4, [1, 4, 4]) == 1
    assert sw.min_sub_array_len(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0

    # Test LC 643
    assert abs(sw.find_max_average([1, 12, -5, -6, 50, 3], 4) - 12.75) < 1e-5

    # Test LC 76
    assert sw.min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert sw.min_window("a", "a") == "a"
    assert sw.min_window("a", "aa") == ""

    print("All Sliding Window Python tests passed successfully!")
