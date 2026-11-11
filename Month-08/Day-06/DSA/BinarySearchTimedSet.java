package Month08.Day06;

/**
 * Timed Set: Binary Search
 * LC 33: Search in Rotated Sorted Array - O(log N) time with half-sorted invariants.
 */
public class BinarySearchTimedSet {

    public static int searchRotated(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;

            // Left half is sorted
            if (nums[left] <= nums[mid]) {
                if (target >= nums[left] && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else { // Right half is sorted
                if (target > nums[mid] && target <= nums[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] nums = {4, 5, 6, 7, 0, 1, 2};
        assert searchRotated(nums, 0) == 4;
        assert searchRotated(nums, 3) == -1;

        System.out.println("Day 06 Binary Search Timed Set verification passed.");
    }
}
