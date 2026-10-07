package DSA;

import java.util.Arrays;

/**
 * Day 25 DSA: Advanced Binary Search Patterns
 * - LeetCode 33: Search in Rotated Sorted Array (O(log N))
 * - LeetCode 153: Find Minimum in Rotated Sorted Array (O(log N))
 * - LeetCode 1011: Capacity To Ship Packages Within D Days (Binary Search on Answer Space)
 */
public class BinarySearchAdvanced {

    /**
     * LC 33: Search in Rotated Sorted Array
     * Time Complexity: O(log N)
     * Space Complexity: O(1)
     */
    public static int searchRotated(int[] nums, int target) {
        if (nums == null || nums.length == 0) return -1;
        int left = 0, right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) return mid;

            // Check if left half is sorted
            if (nums[left] <= nums[mid]) {
                if (target >= nums[left] && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else { // Right half must be sorted
                if (target > nums[mid] && target <= nums[right]) {
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
     * Time Complexity: O(log N)
     * Space Complexity: O(1)
     */
    public static int findMin(int[] nums) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] > nums[right]) {
                // Minimum must lie in the right partition
                left = mid + 1;
            } else {
                // Minimum lies at mid or to the left
                right = mid;
            }
        }
        return nums[left];
    }

    /**
     * LC 1011: Capacity To Ship Packages Within D Days
     * Binary Search on the Answer domain: [max(weights), sum(weights)]
     * Time Complexity: O(N * log(sum - max))
     * Space Complexity: O(1)
     */
    public static int shipWithinDays(int[] weights, int days) {
        int low = 0;
        int high = 0;
        for (int w : weights) {
            low = Math.max(low, w);
            high += w;
        }

        int optimalCapacity = high;
        while (low <= high) {
            int midCapacity = low + (high - low) / 2;
            if (canShipWithCapacity(weights, days, midCapacity)) {
                optimalCapacity = midCapacity;
                high = midCapacity - 1; // Try smaller capacity
            } else {
                low = midCapacity + 1;  // Increase capacity
            }
        }
        return optimalCapacity;
    }

    private static boolean canShipWithCapacity(int[] weights, int days, int capacity) {
        int daysUsed = 1;
        int currentWeight = 0;
        for (int w : weights) {
            if (currentWeight + w > capacity) {
                daysUsed++;
                currentWeight = 0;
            }
            currentWeight += w;
        }
        return daysUsed <= days;
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Day 25: Advanced Binary Search DSA Suite");
        System.out.println("==================================================");

        // Test 1: LC 33 Search Rotated
        int[] rotated = {4, 5, 6, 7, 0, 1, 2};
        int targetIdx = searchRotated(rotated, 0);
        System.out.println("LC 33 (Search in Rotated for 0): Index " + targetIdx);
        assert targetIdx == 4 : "LC 33 Failed";

        // Test 2: LC 153 Find Min
        int minVal = findMin(rotated);
        System.out.println("LC 153 (Find Min in Rotated): " + minVal);
        assert minVal == 0 : "LC 153 Failed";

        // Test 3: LC 1011 Capacity to Ship
        int[] weights = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int days = 5;
        int capacity = shipWithinDays(weights, days);
        System.out.println("LC 1011 (Ship Within 5 Days Capacity): " + capacity);
        assert capacity == 15 : "LC 1011 Failed";

        System.out.println("\nAll Java Binary Search tests executed successfully! [OK]");
    }
}
