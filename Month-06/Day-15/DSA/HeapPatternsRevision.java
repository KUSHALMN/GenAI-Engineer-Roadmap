/**
 * Heap & PriorityQueue Patterns Revision
 * Solves core FAANG interview problems:
 * 1. Kth Largest Element in an Array (LC 215) using Min-Heap
 * 2. Top K Frequent Elements (LC 347)
 * 3. Merge K Sorted Lists (LC 23) in O(N log K) time
 */

import java.util.*;

public class HeapPatternsRevision {

    public static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    // 1. LC 215: Kth Largest Element (Min-Heap of size K)
    public static int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }
        return minHeap.peek();
    }

    // 2. LC 347: Top K Frequent Elements
    public static int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freqMap = new HashMap<>();
        for (int n : nums) freqMap.put(n, freqMap.getOrDefault(n, 0) + 1);

        PriorityQueue<Map.Entry<Integer, Integer>> minHeap =
            new PriorityQueue<>(Comparator.comparingInt(Map.Entry::getValue));

        for (Map.Entry<Integer, Integer> entry : freqMap.entrySet()) {
            minHeap.offer(entry);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }

        int[] result = new int[k];
        for (int i = 0; i < k; i++) {
            result[i] = minHeap.poll().getKey();
        }
        return result;
    }

    // 3. LC 23: Merge K Sorted Lists
    public static ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(Comparator.comparingInt(a -> a.val));
        for (ListNode node : lists) {
            if (node != null) minHeap.offer(node);
        }

        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;

        while (!minHeap.isEmpty()) {
            ListNode smallest = minHeap.poll();
            curr.next = smallest;
            curr = curr.next;
            if (smallest.next != null) {
                minHeap.offer(smallest.next);
            }
        }

        return dummy.next;
    }

    public static void main(String[] args) {
        System.out.println("=== Heap Patterns Verification ===");

        // Test LC 215
        int[] nums1 = {3, 2, 1, 5, 6, 4};
        int kth = findKthLargest(nums1, 2);
        System.out.println("LC 215 (K=2 Largest): " + kth + " (Expected 5)");
        assert kth == 5 : "LC 215 failed";

        // Test LC 347
        int[] nums2 = {1, 1, 1, 2, 2, 3};
        int[] topK = topKFrequent(nums2, 2);
        System.out.println("LC 347 (Top 2 Frequent): " + Arrays.toString(topK));
        assert topK.length == 2 : "LC 347 failed";

        // Test LC 23
        ListNode l1 = buildList(new int[]{1, 4, 5});
        ListNode l2 = buildList(new int[]{1, 3, 4});
        ListNode l3 = buildList(new int[]{2, 6});
        ListNode merged = mergeKLists(new ListNode[]{l1, l2, l3});
        System.out.println("LC 23 (Merged K Lists): " + printList(merged));
        assert merged.val == 1 && merged.next.val == 1 && merged.next.next.val == 2 : "LC 23 failed";

        System.out.println("All Heap pattern tests passed successfully!");
    }

    private static ListNode buildList(int[] vals) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;
        for (int v : vals) {
            curr.next = new ListNode(v);
            curr = curr.next;
        }
        return dummy.next;
    }

    private static String printList(ListNode head) {
        StringBuilder sb = new StringBuilder("[");
        while (head != null) {
            sb.append(head.val);
            if (head.next != null) sb.append(", ");
            head = head.next;
        }
        sb.append("]");
        return sb.toString();
    }
}
