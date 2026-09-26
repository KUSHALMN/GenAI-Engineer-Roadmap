/**
 * Singly Linked List Operations in Java
 *
 * Problems Covered:
 *   1. LeetCode 206 - Reverse Linked List -> O(N) time, O(1) space
 *   2. LeetCode 141 - Linked List Cycle -> O(N) time, O(1) space
 *   3. LeetCode 21  - Merge Two Sorted Lists -> O(N + M) time, O(1) space
 */
public class LinkedListOperations {

    public static class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    /**
     * LC 206: Reverse Linked List
     */
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }
        return prev;
    }

    /**
     * LC 141: Linked List Cycle (Floyd's Tortoise and Hare)
     */
    public boolean hasCycle(ListNode head) {
        if (head == null || head.next == null) return false;
        ListNode slow = head;
        ListNode fast = head.next;

        while (slow != fast) {
            if (fast == null || fast.next == null) return false;
            slow = slow.next;
            fast = fast.next.next;
        }
        return true;
    }

    /**
     * LC 21: Merge Two Sorted Lists
     */
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;

        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                curr.next = list1;
                list1 = list1.next;
            } else {
                curr.next = list2;
                list2 = list2.next;
            }
            curr = curr.next;
        }

        curr.next = (list1 != null) ? list1 : list2;
        return dummy.next;
    }

    // Helper to print list
    public static void printList(ListNode head) {
        ListNode curr = head;
        StringBuilder sb = new StringBuilder();
        while (curr != null) {
            sb.append(curr.val);
            if (curr.next != null) sb.append(" -> ");
            curr = curr.next;
        }
        System.out.println(sb.toString());
    }

    public static void main(String[] args) {
        LinkedListOperations ops = new LinkedListOperations();

        // 1. Reverse list: 1 -> 2 -> 3 -> 4
        ListNode head = new ListNode(1, new ListNode(2, new ListNode(3, new ListNode(4))));
        System.out.print("Original List: ");
        printList(head);
        ListNode rev = ops.reverseList(head);
        System.out.print("Reversed List: ");
        printList(rev);

        // 2. Merge two lists: (1 -> 2 -> 4) and (1 -> 3 -> 4)
        ListNode l1 = new ListNode(1, new ListNode(2, new ListNode(4)));
        ListNode l2 = new ListNode(1, new ListNode(3, new ListNode(4)));
        ListNode merged = ops.mergeTwoLists(l1, l2);
        System.out.print("Merged List: ");
        printList(merged);

        // 3. Cycle Detection
        ListNode c1 = new ListNode(10);
        ListNode c2 = new ListNode(20);
        c1.next = c2;
        c2.next = c1;
        System.out.println("Has Cycle: " + ops.hasCycle(c1)); // true
    }
}
