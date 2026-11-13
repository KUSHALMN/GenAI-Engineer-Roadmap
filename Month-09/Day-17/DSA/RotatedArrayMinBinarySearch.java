package Month_09.Day_17.DSA;

/**
 * Day 17: Timed DSA Problem Set — Binary Search in Rotated Sorted Array with Duplicates.
 * Focus: LeetCode 154 (Find Minimum in Rotated Sorted Array II) - Average O(log N), Worst O(N).
 */
public class RotatedArrayMinBinarySearch {

    public static int findMin(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int left = 0, right = nums.length - 1;

        while (left < right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] < nums[right]) {
                // Minimum is in the left half including mid
                right = mid;
            } else if (nums[mid] > nums[right]) {
                // Minimum is strictly in the right half
                left = mid + 1;
            } else {
                // nums[mid] == nums[right]: duplicate ambiguity, decrement right safely
                right--;
            }
        }
        return nums[left];
    }

    public static void main(String[] args) {
        assert findMin(new int[]{1, 3, 5}) == 1 : "Test 1 Failed";
        assert findMin(new int[]{2, 2, 2, 0, 1}) == 0 : "Test 2 Failed";
        assert findMin(new int[]{3, 1, 3}) == 1 : "Test 3 Failed";
        assert findMin(new int[]{10, 1, 10, 10, 10}) == 1 : "Test 4 Failed";

        System.out.println("Day 17 Rotated Array Min Binary Search verification passed.");
    }
}
