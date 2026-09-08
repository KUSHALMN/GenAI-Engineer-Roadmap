import java.util.PriorityQueue;

/**
 * Problem: Merge k Sorted Lists (LeetCode 23 - Hard / High Frequency FAANG)
 * 
 * You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
 * Merge all the linked-lists into one sorted linked-list and return it.
 * 
 * Approaches:
 * 1. Min-Heap (PriorityQueue):
 *    - Insert the head node of all k lists into a min-heap.
 *    - Repeatedly extract the minimum node, append to merged list, and offer next node.
 *    - Time Complexity: O(N * log k) where N is total nodes, k is number of lists.
 *    - Space Complexity: O(k) for the priority queue.
 * 
 * 2. Divide and Conquer:
 *    - Pair up k lists and merge each pair using standard two-list merge.
 *    - Repeat until only one merged list remains.
 *    - Time Complexity: O(N * log k)
 *    - Space Complexity: O(1) iterative or O(log k) recursive call stack.
 */
public class merge_k_sorted_lists {

    public static class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    // ==========================================
    // Approach 1: Min-Heap (PriorityQueue)
    // ==========================================
    public static ListNode mergeKListsHeap(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        PriorityQueue<ListNode> pq = new PriorityQueue<>(lists.length, (a, b) -> Integer.compare(a.val, b.val));

        // Add non-null list heads to heap
        for (ListNode head : lists) {
            if (head != null) {
                pq.offer(head);
            }
        }

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;

        while (!pq.isEmpty()) {
            ListNode minNode = pq.poll();
            tail.next = minNode;
            tail = tail.next;

            if (minNode.next != null) {
                pq.offer(minNode.next);
            }
        }

        return dummy.next;
    }

    // ==========================================
    // Approach 2: Divide and Conquer
    // ==========================================
    public static ListNode mergeKListsDivideAndConquer(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;
        int interval = 1;
        while (interval < lists.length) {
            for (int i = 0; i + interval < lists.length; i += interval * 2) {
                lists[i] = mergeTwoLists(lists[i], lists[i + interval]);
            }
            interval *= 2;
        }
        return lists[0];
    }

    private static ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                curr.next = l1;
                l1 = l1.next;
            } else {
                curr.next = l2;
                l2 = l2.next;
            }
            curr = curr.next;
        }
        curr.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }

    // Helper: Build list from array
    public static ListNode buildList(int[] arr) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;
        for (int val : arr) {
            curr.next = new ListNode(val);
            curr = curr.next;
        }
        return dummy.next;
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 23: Merge k Sorted Lists (Java)");
        System.out.println("=================================================");

        // Test 1: [[1,4,5],[1,3,4],[2,6]]
        ListNode[] lists1 = new ListNode[] {
            buildList(new int[]{1, 4, 5}),
            buildList(new int[]{1, 3, 4}),
            buildList(new int[]{2, 6})
        };
        ListNode merged1 = mergeKListsHeap(lists1);

        StringBuilder sb = new StringBuilder();
        while (merged1 != null) {
            sb.append(merged1.val).append(merged1.next != null ? "->" : "");
            merged1 = merged1.next;
        }
        System.out.println("Test 1 Merged result: " + sb);
        assert sb.toString().equals("1->1->2->3->4->4->5->6") : "Failed Test 1";

        // Test 2: Empty lists array
        ListNode merged2 = mergeKListsHeap(new ListNode[]{});
        assert merged2 == null : "Failed Test 2";

        // Test 3: Array of empty heads
        ListNode merged3 = mergeKListsHeap(new ListNode[]{null, null});
        assert merged3 == null : "Failed Test 3";

        System.out.println("\n✅ All Merge k Sorted Lists tests passed successfully!");
    }
}
