package Month08.Day07;

/**
 * Timed Set: Linked Lists
 * LC 206: Reverse Linked List - O(N) time and O(1) space with iterative 3-pointer swap.
 */
public class LinkedListsTimedSet {

    public static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public static ListNode reverseList(ListNode head) {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }
        return prev;
    }

    public static void main(String[] args) {
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);

        ListNode rev = reverseList(head);
        assert rev.val == 3;
        assert rev.next.val == 2;
        assert rev.next.next.val == 1;

        System.out.println("Day 07 Linked Lists Timed Set verification passed.");
    }
}
