package Month08.Day11;

import java.util.PriorityQueue;

/**
 * Timed Set: Heaps & Top K
 * LC 215: Kth Largest Element in an Array - O(N log K) time with min-heap of size K.
 */
public class HeapsTopKTimedSet {

    public static int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);
        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }
        return minHeap.peek();
    }

    public static void main(String[] args) {
        int[] nums = {3, 2, 1, 5, 6, 4};
        assert findKthLargest(nums, 2) == 5;

        int[] nums2 = {3, 2, 3, 1, 2, 4, 5, 5, 6};
        assert findKthLargest(nums2, 4) == 4;

        System.out.println("Day 11 Heaps & Top K Timed Set verification passed.");
    }
}
