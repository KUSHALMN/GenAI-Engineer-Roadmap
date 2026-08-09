public class reverse_linked_list {
    // LeetCode #206 - Reverse Linked List
    // Approach: Iterative Two Pointers O(n)

    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public ListNode reverseList(ListNode head) {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }

    static void print(ListNode head) {
        while (head != null) {
            System.out.print(head.val + (head.next != null ? " -> " : "\n"));
            head = head.next;
        }
    }

    public static void main(String[] args) {
        reverse_linked_list sol = new reverse_linked_list();
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);
        head.next.next.next.next = new ListNode(5);
        print(sol.reverseList(head)); // 5 -> 4 -> 3 -> 2 -> 1
    }
}
