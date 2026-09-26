import java.util.*;

/**
 * Heap & Priority Queue Patterns in Java
 *
 * Problems Covered:
 *   1. LeetCode 215 - Kth Largest Element in an Array -> O(N log K) time, O(K) space
 *   2. LeetCode 347 - Top K Frequent Elements -> O(N log K) time, O(N) space
 *   3. LeetCode 23  - Merge K Sorted Lists -> O(N log K) time, O(K) space
 */
public class HeapPatterns {

    public static class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    /**
     * LC 215: Kth Largest Element in an Array (Min-Heap of size k)
     */
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);
        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }
        return minHeap.peek();
    }

    /**
     * LC 347: Top K Frequent Elements
     */
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> countMap = new HashMap<>();
        for (int num : nums) {
            countMap.put(num, countMap.getOrDefault(num, 0) + 1);
        }

        // Min-heap ordered by frequency ascending
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(
            Comparator.comparingInt(countMap::get)
        );

        for (int num : countMap.keySet()) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }

        int[] result = new int[k];
        for (int i = k - 1; i >= 0; i--) {
            result[i] = minHeap.poll();
        }
        return result;
    }

    /**
     * LC 23: Merge K Sorted Lists
     */
    public ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
            Comparator.comparingInt(node -> node.val)
        );

        for (ListNode node : lists) {
            if (node != null) {
                minHeap.offer(node);
            }
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
        HeapPatterns hp = new HeapPatterns();

        // 1. LC 215
        int kth = hp.findKthLargest(new int[]{3, 2, 1, 5, 6, 4}, 2);
        System.out.println("LC 215 2nd Largest: " + kth); // 5

        // 2. LC 347
        int[] top2 = hp.topKFrequent(new int[]{1, 1, 1, 2, 2, 3}, 2);
        System.out.println("LC 347 Top 2 Frequent: " + Arrays.toString(top2)); // [1, 2]

        // 3. LC 23
        ListNode l1 = new ListNode(1, new ListNode(4, new ListNode(5)));
        ListNode l2 = new ListNode(1, new ListNode(3, new ListNode(4)));
        ListNode l3 = new ListNode(2, new ListNode(6));
        ListNode merged = hp.mergeKLists(new ListNode[]{l1, l2, l3});

        System.out.print("LC 23 Merged: ");
        ListNode c = merged;
        while (c != null) {
            System.out.print(c.val + (c.next != null ? "->" : ""));
            c = c.next;
        }
        System.out.println();
    }
}
