/**
 * Binary Search Patterns Revision
 * Solves core FAANG interview binary search patterns:
 * 1. Find First and Last Position in Sorted Array (LC 34)
 * 2. Search in Rotated Sorted Array (LC 33)
 * 3. Find Peak Element (LC 162)
 */

import java.util.Arrays;

public class BinarySearchPatternsRevision {

    // 1. LC 34: Find First and Last Position
    public static int[] searchRange(int[] nums, int target) {
        int first = findBound(nums, target, true);
        if (first == -1) return new int[]{-1, -1};
        int last = findBound(nums, target, false);
        return new int[]{first, last};
    }

    private static int findBound(int[] nums, int target, boolean isFirst) {
        int low = 0, high = nums.length - 1;
        int ans = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) {
                ans = mid;
                if (isFirst) {
                    high = mid - 1; // Search left
                } else {
                    low = mid + 1;  // Search right
                }
            } else if (nums[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return ans;
    }

    // 2. LC 33: Search in Rotated Sorted Array (Distinct Elements)
    public static int searchRotated(int[] nums, int target) {
        int low = 0, high = nums.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) return mid;

            // Check if left half is sorted
            if (nums[low] <= nums[mid]) {
                if (target >= nums[low] && target < nums[mid]) {
                    high = mid - 1;
                } else {
                    low = mid + 1;
                }
            } else { // Right half is sorted
                if (target > nums[mid] && target <= nums[high]) {
                    low = mid + 1;
                } else {
                    high = mid - 1;
                }
            }
        }
        return -1;
    }

    // 3. LC 162: Find Peak Element
    public static int findPeakElement(int[] nums) {
        int low = 0, high = nums.length - 1;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] > nums[mid + 1]) {
                high = mid; // Peak is at mid or to the left
            } else {
                low = mid + 1; // Slope rising to the right
            }
        }
        return low;
    }

    public static void main(String[] args) {
        System.out.println("=== Binary Search Patterns Verification ===");

        // Test LC 34
        int[] nums1 = {5, 7, 7, 8, 8, 10};
        int[] range = searchRange(nums1, 8);
        System.out.println("LC 34 (Target 8): " + Arrays.toString(range));
        assert range[0] == 3 && range[1] == 4 : "LC 34 failed";

        // Test LC 33
        int[] nums2 = {4, 5, 6, 7, 0, 1, 2};
        int idx = searchRotated(nums2, 0);
        System.out.println("LC 33 (Target 0 in Rotated): " + idx);
        assert idx == 4 : "LC 33 failed";

        // Test LC 162
        int[] nums3 = {1, 2, 1, 3, 5, 6, 4};
        int peak = findPeakElement(nums3);
        System.out.println("LC 162 (Peak Index): " + peak + " (Value: " + nums3[peak] + ")");
        assert peak == 5 || peak == 1 : "LC 162 failed";

        System.out.println("All Binary Search patterns passed successfully!");
    }
}
