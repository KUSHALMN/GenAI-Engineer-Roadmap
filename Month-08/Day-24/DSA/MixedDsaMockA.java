package Month_08.Day_24.DSA;

import java.util.PriorityQueue;

/**
 * Day 24: Timed DSA Problem Set — Mixed Hard Mock Set A.
 * Focus: LeetCode 42 (Trapping Rain Water) & LeetCode 23 (Merge k Sorted Lists).
 */
public class MixedDsaMockA {

    // LeetCode 42: Trapping Rain Water - O(N) Time, O(1) Space (Two Pointers)
    public static int trap(int[] height) {
        if (height == null || height.length < 3) return 0;
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0;
        int trapped = 0;

        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) {
                    leftMax = height[left];
                } else {
                    trapped += leftMax - height[left];
                }
                left++;
            } else {
                if (height[right] >= rightMax) {
                    rightMax = height[right];
                } else {
                    trapped += rightMax - height[right];
                }
                right--;
            }
        }
        return trapped;
    }

    // LeetCode 23: Merge k Sorted Lists Node
    public static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    // O(N log k) Time, O(k) Space Min-Heap
    public static ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;
        PriorityQueue<ListNode> pq = new PriorityQueue<>(lists.length, (a, b) -> Integer.compare(a.val, b.val));

        for (ListNode node : lists) {
            if (node != null) pq.offer(node);
        }

        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;

        while (!pq.isEmpty()) {
            ListNode smallest = pq.poll();
            curr.next = smallest;
            curr = curr.next;
            if (smallest.next != null) {
                pq.offer(smallest.next);
            }
        }
        return dummy.next;
    }

    public static void main(String[] args) {
        // LC 42 tests
        assert trap(new int[]{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1}) == 6 : "Trap Test 1 Failed";
        assert trap(new int[]{4, 2, 0, 3, 2, 5}) == 9 : "Trap Test 2 Failed";

        // LC 23 tests
        ListNode l1 = new ListNode(1); l1.next = new ListNode(4); l1.next.next = new ListNode(5);
        ListNode l2 = new ListNode(1); l2.next = new ListNode(3); l2.next.next = new ListNode(4);
        ListNode l3 = new ListNode(2); l3.next = new ListNode(6);

        ListNode merged = mergeKLists(new ListNode[]{l1, l2, l3});
        int[] expected = {1, 1, 2, 3, 4, 4, 5, 6};
        int idx = 0;
        while (merged != null) {
            assert merged.val == expected[idx++] : "MergeKLists value mismatch";
            merged = merged.next;
        }

        System.out.println("Day 24 Mixed Hard Mock Set A verification passed.");
    }
}
