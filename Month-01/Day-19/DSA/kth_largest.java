import java.util.PriorityQueue;
import java.util.Random;
import java.util.Arrays;

/**
 * Problem: Kth Largest Element in an Array (LeetCode 215)
 * 
 * Approaches:
 * 1. Min-Heap Approach (PriorityQueue):
 *    - Maintain a Min-Heap of size K.
 *    - If heap size exceeds K, poll the smallest element.
 *    - At the end, the top of the Min-Heap is the K-th largest element.
 *    - Time Complexity: O(N log K)
 *    - Space Complexity: O(K)
 * 
 * 2. QuickSelect (Hoare's Selection Algorithm):
 *    - Partition array around a random pivot (similar to QuickSort).
 *    - Recurse only on the partition containing the target index (N - K).
 *    - Time Complexity: O(N) average, O(N^2) worst case.
 *    - Space Complexity: O(1) iterative or O(log N) recursive stack.
 */
public class kth_largest {

    // Approach 1: Min-Heap
    public static int findKthLargestMinHeap(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0 || k > nums.length) {
            throw new IllegalArgumentException("Invalid input array or k value");
        }

        // Min-Heap keeps smallest of the K largest elements at the top
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);

        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }

        return minHeap.peek();
    }

    // Approach 2: QuickSelect (Average O(N))
    public static int findKthLargestQuickSelect(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0 || k > nums.length) {
            throw new IllegalArgumentException("Invalid input array or k value");
        }

        int targetIndex = nums.length - k; // Target index in 0-indexed sorted array
        int left = 0;
        int right = nums.length - 1;
        Random rand = new Random();

        while (left <= right) {
            int pivotIndex = left + rand.nextInt(right - left + 1);
            int finalPivotIndex = partition(nums, left, right, pivotIndex);

            if (finalPivotIndex == targetIndex) {
                return nums[finalPivotIndex];
            } else if (finalPivotIndex < targetIndex) {
                left = finalPivotIndex + 1;
            } else {
                right = finalPivotIndex - 1;
            }
        }

        return -1;
    }

    private static int partition(int[] nums, int left, int right, int pivotIndex) {
        int pivotValue = nums[pivotIndex];
        // Move pivot to end
        swap(nums, pivotIndex, right);
        int storeIndex = left;

        for (int i = left; i < right; i++) {
            if (nums[i] < pivotValue) {
                swap(nums, storeIndex, i);
                storeIndex++;
            }
        }

        // Move pivot to its final sorted position
        swap(nums, storeIndex, right);
        return storeIndex;
    }

    private static void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }

    public static void main(String[] args) {
        System.out.println("=== Kth Largest Element in an Array ===");

        int[][] testCases = {
            {3, 2, 1, 5, 6, 4},
            {3, 2, 3, 1, 2, 4, 5, 5, 6},
            {1},
            {7, 10, 4, 3, 20, 15},
            {-1, -2, 0, 5, 3}
        };
        int[] kValues = {2, 4, 1, 3, 2};

        for (int i = 0; i < testCases.length; i++) {
            int[] numsCopy1 = Arrays.copyOf(testCases[i], testCases[i].length);
            int[] numsCopy2 = Arrays.copyOf(testCases[i], testCases[i].length);
            int k = kValues[i];

            int resHeap = findKthLargestMinHeap(numsCopy1, k);
            int resSelect = findKthLargestQuickSelect(numsCopy2, k);

            System.out.println("\nTest Case " + (i + 1) + ":");
            System.out.println("Array: " + Arrays.toString(testCases[i]) + ", k = " + k);
            System.out.println("Min-Heap Result:    " + resHeap);
            System.out.println("QuickSelect Result: " + resSelect);
            assert resHeap == resSelect : "Results do not match!";
        }

        System.out.println("\nAll test cases passed successfully!");
    }
}
