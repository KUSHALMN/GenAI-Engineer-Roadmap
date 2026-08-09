public class middle_of_linked_list {
    // LeetCode #876 - Middle of the Linked List
    // Approach: Fast & Slow Pointers O(n)

    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public ListNode middleNode(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    public static void main(String[] args) {
        middle_of_linked_list sol = new middle_of_linked_list();

        // [1,2,3,4,5] → middle = 3
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);
        head.next.next.next.next = new ListNode(5);
        System.out.println(sol.middleNode(head).val); // 3

        // [1,2,3,4,5,6] → middle = 4
        ListNode head2 = new ListNode(1);
        head2.next = new ListNode(2);
        head2.next.next = new ListNode(3);
        head2.next.next.next = new ListNode(4);
        head2.next.next.next.next = new ListNode(5);
        head2.next.next.next.next.next = new ListNode(6);
        System.out.println(sol.middleNode(head2).val); // 4
    }
}
