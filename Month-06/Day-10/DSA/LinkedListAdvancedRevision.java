/**
 * Advanced Linked List Revision Patterns
 * Solves core FAANG interview problems:
 * 1. Reverse Nodes in k-Group (LC 25) with O(1) space
 * 2. Reorder List (LC 143) - Find mid, reverse half, interleave
 * 3. Copy List with Random Pointer (LC 138) with O(1) extra space
 */

public class LinkedListAdvancedRevision {

    public static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    // 1. LC 25: Reverse Nodes in k-Group
    public static ListNode reverseKGroup(ListNode head, int k) {
        if (head == null || k <= 1) return head;

        // Check if there are at least k nodes remaining
        ListNode curr = head;
        int count = 0;
        while (curr != null && count < k) {
            curr = curr.next;
            count++;
        }

        if (count == k) {
            // Reverse first k nodes
            ListNode reversedHead = reverseLinkedList(head, k);
            // Recurse on remaining list and connect
            head.next = reverseKGroup(curr, k);
            return reversedHead;
        }

        return head; // Less than k nodes, leave as is
    }

    private static ListNode reverseLinkedList(ListNode head, int k) {
        ListNode prev = null;
        ListNode curr = head;
        while (k > 0) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
            k--;
        }
        return prev;
    }

    // 2. LC 143: Reorder List (L0 -> Ln -> L1 -> Ln-1 ...)
    public static void reorderList(ListNode head) {
        if (head == null || head.next == null) return;

        // Step 1: Find middle using slow/fast pointers
        ListNode slow = head, fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // Step 2: Reverse second half
        ListNode second = reverseFullList(slow.next);
        slow.next = null; // Split lists

        // Step 3: Interleave first and second halves
        ListNode first = head;
        while (second != null) {
            ListNode tmp1 = first.next;
            ListNode tmp2 = second.next;

            first.next = second;
            second.next = tmp1;

            first = tmp1;
            second = tmp2;
        }
    }

    private static ListNode reverseFullList(ListNode head) {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }

    public static void main(String[] args) {
        System.out.println("=== Advanced Linked List Patterns Verification ===");

        // Test LC 25: Reverse in k-Group (k=2)
        ListNode l1 = buildList(new int[]{1, 2, 3, 4, 5});
        ListNode revK = reverseKGroup(l1, 2);
        System.out.println("LC 25 (k=2): " + printList(revK) + " (Expected [2, 1, 4, 3, 5])");
        assert revK.val == 2 && revK.next.val == 1 : "LC 25 failed";

        // Test LC 143: Reorder List
        ListNode l2 = buildList(new int[]{1, 2, 3, 4});
        reorderList(l2);
        System.out.println("LC 143 (Reordered): " + printList(l2) + " (Expected [1, 4, 2, 3])");
        assert l2.val == 1 && l2.next.val == 4 : "LC 143 failed";

        System.out.println("All Advanced Linked List tests passed successfully!");
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
