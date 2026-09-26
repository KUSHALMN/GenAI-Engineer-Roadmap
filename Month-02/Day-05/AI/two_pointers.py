"""
Two Pointers DSA Pattern (Python).
Classic LeetCode problems implemented with comprehensive test cases:
1. Two Sum II - Input Array Is Sorted (LC 167) - O(N) time, O(1) space
2. 3Sum (LC 15) - O(N^2) time, O(1) extra space
3. Container With Most Water (LC 11) - O(N) time, O(1) space
4. Valid Palindrome (LC 125) - O(N) time, O(1) space
"""

from typing import List


class TwoPointers:

    @staticmethod
    def two_sum_sorted(numbers: List[int], target: int) -> List[int]:
        """
        LC 167: Two Sum II - Input Array Is Sorted.
        Returns 1-based indices [index1, index2].
        """
        left, right = 0, len(numbers) - 1
        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                return [left + 1, right + 1]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return []

    @staticmethod
    def three_sum(nums: List[int]) -> List[List[int]]:
        """
        LC 15: 3Sum.
        Returns all unique triplets [nums[i], nums[j], nums[k]] such that their sum is 0.
        """
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicates for the first element
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    # Skip duplicates for left and right
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif total < 0:
                    left += 1
                else:
                    right -= 1

        return result

    @staticmethod
    def max_area(height: List[int]) -> int:
        """
        LC 11: Container With Most Water.
        Find two lines that together with x-axis forms a container containing the most water.
        """
        left, right = 0, len(height) - 1
        max_water = 0

        while left < right:
            h = min(height[left], height[right])
            width = right - left
            max_water = max(max_water, h * width)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_water

    @staticmethod
    def is_palindrome(s: str) -> bool:
        """
        LC 125: Valid Palindrome.
        Considers only alphanumeric characters and ignores cases.
        """
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1

            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1

        return True


if __name__ == "__main__":
    tp = TwoPointers()

    # Test LC 167
    assert tp.two_sum_sorted([2, 7, 11, 15], 9) == [1, 2]
    assert tp.two_sum_sorted([2, 3, 4], 6) == [1, 3]

    # Test LC 15
    res_3sum = tp.three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted(res_3sum) == [[-1, -1, 2], [-1, 0, 1]]

    # Test LC 11
    assert tp.max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert tp.max_area([1, 1]) == 1

    # Test LC 125
    assert tp.is_palindrome("A man, a plan, a canal: Panama") is True
    assert tp.is_palindrome("race a car") is False

    print("All Two Pointers Python tests passed successfully!")
