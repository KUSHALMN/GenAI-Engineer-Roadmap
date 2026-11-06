import java.util.*;

/**
 * Day 24: Quickselect — Kth Largest Element in an Array
 * Problem: Given an integer array nums and an integer k, return the kth largest element in the array.
 *
 * Algorithm:
 * - Quickselect partition algorithm with average O(n) runtime.
 * - Target index is nums.length - k in sorted order.
 *
 * Time Complexity: Average O(n), Worst Case O(n^2)
 * Space Complexity: O(1) auxiliary.
 */
public class KthLargestElement {

    public int findKthLargest(int[] nums, int k) {
        int targetIdx = nums.length - k;
        return quickSelect(nums, 0, nums.length - 1, targetIdx);
    }

    private int quickSelect(int[] nums, int left, int right, int k) {
        if (left == right) return nums[left];

        int pivotIndex = partition(nums, left, right);
        if (pivotIndex == k) {
            return nums[k];
        } else if (pivotIndex < k) {
            return quickSelect(nums, pivotIndex + 1, right, k);
        } else {
            return quickSelect(nums, left, pivotIndex - 1, k);
        }
    }

    private int partition(int[] nums, int left, int right) {
        int pivot = nums[right];
        int i = left;
        for (int j = left; j < right; j++) {
            if (nums[j] <= pivot) {
                swap(nums, i++, j);
            }
        }
        swap(nums, i, right);
        return i;
    }

    private void swap(int[] nums, int i, int j) {
        int t = nums[i]; nums[i] = nums[j]; nums[j] = t;
    }

    public static void main(String[] args) {
        KthLargestElement solver = new KthLargestElement();
        int[] nums = {3, 2, 1, 5, 6, 4};
        int k = 2;
        int kth = solver.findKthLargest(nums, k);

        System.out.println("2nd largest element in [3, 2, 1, 5, 6, 4]: " + kth);
        assert kth == 5 : "Expected 5";
        System.out.println("Day 24 DSA KthLargestElement verification passed!");
    }
}
