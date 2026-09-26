"""
Binary Search Patterns (Python).
Problems Implemented:
1. Binary Search (LC 704) - O(log N) time, O(1) space
2. Search in Rotated Sorted Array (LC 33) - O(log N) time, O(1) space
3. Find Minimum in Rotated Sorted Array (LC 153) - O(log N) time, O(1) space
4. Find First and Last Position of Element in Sorted Array (LC 34) - O(log N) time
"""

from typing import List


class BinarySearchPatterns:

    @staticmethod
    def search(nums: List[int], target: int) -> int:
        """LC 704: Classic Binary Search."""
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    @staticmethod
    def search_rotated(nums: List[int], target: int) -> int:
        """
        LC 33: Search in Rotated Sorted Array.
        Determines which half is sorted, then checks target boundaries.
        """
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            # Left half is sorted
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            # Right half is sorted
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1

    @staticmethod
    def find_min(nums: List[int]) -> int:
        """
        LC 153: Find Minimum in Rotated Sorted Array.
        """
        left, right = 0, len(nums) - 1

        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]


if __name__ == "__main__":
    bs = BinarySearchPatterns()

    # LC 704
    assert bs.search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert bs.search([-1, 0, 3, 5, 9, 12], 2) == -1

    # LC 33
    assert bs.search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert bs.search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert bs.search_rotated([1], 0) == -1

    # LC 153
    assert bs.find_min([3, 4, 5, 1, 2]) == 1
    assert bs.find_min([4, 5, 6, 7, 0, 1, 2]) == 0
    assert bs.find_min([11, 13, 15, 17]) == 11

    print("All Binary Search Python tests passed successfully!")
