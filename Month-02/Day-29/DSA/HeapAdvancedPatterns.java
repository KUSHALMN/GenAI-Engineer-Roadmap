package DSA;

import java.util.*;

/**
 * Day 29 DSA: Advanced Heap & Priority Queue Patterns
 * - LeetCode 23: Merge k Sorted Lists (O(N log K))
 * - LeetCode 347: Top K Frequent Elements (Min-Heap O(N log K))
 * - LeetCode 295: Find Median from Data Stream (Two Heaps: Max-Heap & Min-Heap)
 */
public class HeapAdvancedPatterns {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) {
            this.val = val;
        }
    }

    // -----------------------------------------------------------------
    // LC 23: Merge k Sorted Lists
    // -----------------------------------------------------------------
    public static ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
            Comparator.comparingInt(node -> node.val)
        );

        for (ListNode head : lists) {
            if (head != null) minHeap.offer(head);
        }

        ListNode dummy = new ListNode(0);
        ListNode current = dummy;

        while (!minHeap.isEmpty()) {
            ListNode smallest = minHeap.poll();
            current.next = smallest;
            current = current.next;

            if (smallest.next != null) {
                minHeap.offer(smallest.next);
            }
        }
        return dummy.next;
    }

    // -----------------------------------------------------------------
    // LC 347: Top K Frequent Elements
    // -----------------------------------------------------------------
    public static int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> countMap = new HashMap<>();
        for (int num : nums) {
            countMap.put(num, countMap.getOrDefault(num, 0) + 1);
        }

        // Min-Heap keeping top k frequent entries
        PriorityQueue<Map.Entry<Integer, Integer>> minHeap = new PriorityQueue<>(
            Comparator.comparingInt(Map.Entry::getValue)
        );

        for (Map.Entry<Integer, Integer> entry : countMap.entrySet()) {
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

    // -----------------------------------------------------------------
    // LC 295: MedianFinder using Dual Heaps
    // -----------------------------------------------------------------
    public static class MedianFinder {
        // lower half: stores smaller numbers in descending order (max-heap)
        private final PriorityQueue<Integer> lowerMaxHeap;
        // upper half: stores larger numbers in ascending order (min-heap)
        private final PriorityQueue<Integer> upperMinHeap;

        public MedianFinder() {
            lowerMaxHeap = new PriorityQueue<>(Collections.reverseOrder());
            upperMinHeap = new PriorityQueue<>();
        }

        public void addNum(int num) {
            lowerMaxHeap.offer(num);
            upperMinHeap.offer(lowerMaxHeap.poll());

            // Balance sizes: lowerMaxHeap may have at most 1 more element than upperMinHeap
            if (lowerMaxHeap.size() < upperMinHeap.size()) {
                lowerMaxHeap.offer(upperMinHeap.poll());
            }
        }

        public double findMedian() {
            if (lowerMaxHeap.size() > upperMinHeap.size()) {
                return lowerMaxHeap.peek();
            }
            return (lowerMaxHeap.peek() + upperMinHeap.peek()) / 2.0;
        }
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Day 29: Advanced Heap & Priority Queue DSA Suite");
        System.out.println("==================================================");

        // Test 1: LC 23 Merge k Lists
        ListNode l1 = new ListNode(1); l1.next = new ListNode(4); l1.next.next = new ListNode(5);
        ListNode l2 = new ListNode(1); l2.next = new ListNode(3); l2.next.next = new ListNode(4);
        ListNode l3 = new ListNode(2); l3.next = new ListNode(6);
        ListNode merged = mergeKLists(new ListNode[]{l1, l2, l3});

        List<Integer> mergedVals = new ArrayList<>();
        while (merged != null) {
            mergedVals.add(merged.val);
            merged = merged.next;
        }
        System.out.println("LC 23 Merged K Lists: " + mergedVals);
        assert mergedVals.equals(Arrays.asList(1, 1, 2, 3, 4, 4, 5, 6)) : "LC 23 Failed";

        // Test 2: LC 347 Top K Frequent
        int[] nums = {1, 1, 1, 2, 2, 3};
        int[] topK = topKFrequent(nums, 2);
        System.out.println("LC 347 Top 2 Frequent: " + Arrays.toString(topK));
        Set<Integer> expectedTop = new HashSet<>(Arrays.asList(1, 2));
        assert expectedTop.contains(topK[0]) && expectedTop.contains(topK[1]) : "LC 347 Failed";

        // Test 3: LC 295 MedianFinder
        MedianFinder mf = new MedianFinder();
        mf.addNum(1);
        mf.addNum(2);
        double med1 = mf.findMedian();
        System.out.println("LC 295 Median of [1, 2]: " + med1);
        assert med1 == 1.5 : "Median 1.5 Failed";

        mf.addNum(3);
        double med2 = mf.findMedian();
        System.out.println("LC 295 Median of [1, 2, 3]: " + med2);
        assert med2 == 2.0 : "Median 2.0 Failed";

        System.out.println("\nAll Java Heap tests executed successfully! [OK]");
    }
}
