/**
 * Binary Search Patterns in Java
 *
 * Problems Covered:
 *   1. LeetCode 704 - Binary Search -> O(log N) time, O(1) space
 *   2. LeetCode 33  - Search in Rotated Sorted Array -> O(log N) time, O(1) space
 *   3. LeetCode 153 - Find Minimum in Rotated Sorted Array -> O(log N) time, O(1) space
 */
public class BinarySearchPatterns {

    /**
     * LC 704: Standard Binary Search
     */
    public int search(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }

    /**
     * LC 33: Search in Rotated Sorted Array
     */
    public int searchRotated(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            }

            // Left side is normally sorted
            if (nums[left] <= nums[mid]) {
                if (nums[left] <= target && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else {
                // Right side is normally sorted
                if (nums[mid] < target && target <= nums[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }
        return -1;
    }

    /**
     * LC 153: Find Minimum in Rotated Sorted Array
     */
    public int findMin(int[] nums) {
        int left = 0;
        int right = nums.length - 1;

        while (left < right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] > nums[right]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return nums[left];
    }

    public static void main(String[] args) {
        BinarySearchPatterns bs = new BinarySearchPatterns();

        // 1. LC 704
        int idx1 = bs.search(new int[]{-1, 0, 3, 5, 9, 12}, 9);
        System.out.println("LC 704 Search 9: " + idx1); // 4

        // 2. LC 33
        int idx2 = bs.searchRotated(new int[]{4, 5, 6, 7, 0, 1, 2}, 0);
        System.out.println("LC 33 Search 0: " + idx2); // 4

        // 3. LC 153
        int minVal = bs.findMin(new int[]{4, 5, 6, 7, 0, 1, 2});
        System.out.println("LC 153 Min Value: " + minVal); // 0
    }
}
