/**
 * Day 26 DSA: Fast & Slow Pointer (Floyd's Cycle Finding) Patterns
 * - LeetCode 141: Linked List Cycle (Detection)
 * - LeetCode 142: Linked List Cycle II (Find Start Node of Cycle)
 * - LeetCode 234: Palindrome Linked List (O(1) auxiliary space)
 */
public class LinkedListCyclePatterns {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) {
            this.val = val;
            this.next = null;
        }
    }

    /**
     * LC 141: Detect if cycle exists in linked list
     * Time: O(N), Space: O(1)
     */
    public static boolean hasCycle(ListNode head) {
        if (head == null || head.next == null) return false;
        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }

    /**
     * LC 142: Find the node where cycle begins
     * Mathematical proof: Distance from head to cycle entry equals distance from meeting point to cycle entry.
     * Time: O(N), Space: O(1)
     */
    public static ListNode detectCycle(ListNode head) {
        if (head == null || head.next == null) return null;
        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                // Cycle detected, find intersection entry point
                ListNode ptr1 = head;
                ListNode ptr2 = slow;
                while (ptr1 != ptr2) {
                    ptr1 = ptr1.next;
                    ptr2 = ptr2.next;
                }
                return ptr1;
            }
        }
        return null;
    }

    /**
     * LC 234: Palindrome Linked List
     * Steps: 1. Find midpoint (slow/fast), 2. Reverse second half, 3. Compare both halves.
     * Time: O(N), Space: O(1)
     */
    public static boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) return true;

        // 1. Find midpoint
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // 2. Reverse second half
        ListNode prev = null;
        ListNode curr = slow;
        while (curr != null) {
            ListNode nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }

        // 3. Compare halves
        ListNode firstHalf = head;
        ListNode secondHalf = prev;
        while (secondHalf != null) {
            if (firstHalf.val != secondHalf.val) return false;
            firstHalf = firstHalf.next;
            secondHalf = secondHalf.next;
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Day 26: Fast & Slow Pointer Linked List Suite");
        System.out.println("==================================================");

        // Test 1 & 2: Cycle detection and entry point
        // 3 -> 2 -> 0 -> -4 (points back to 2)
        ListNode head = new ListNode(3);
        ListNode node2 = new ListNode(2);
        ListNode node0 = new ListNode(0);
        ListNode nodeN4 = new ListNode(-4);
        head.next = node2;
        node2.next = node0;
        node0.next = nodeN4;
        nodeN4.next = node2; // cycle to node2

        boolean cycleExists = hasCycle(head);
        System.out.println("LC 141 (Has Cycle): " + cycleExists);
        assert cycleExists : "LC 141 failed";

        ListNode entry = detectCycle(head);
        System.out.println("LC 142 (Cycle Entry Node Val): " + (entry != null ? entry.val : "null"));
        assert entry != null && entry.val == 2 : "LC 142 failed";

        // Test 3: Palindrome Linked List
        // 1 -> 2 -> 2 -> 1
        ListNode pHead = new ListNode(1);
        pHead.next = new ListNode(2);
        pHead.next.next = new ListNode(2);
        pHead.next.next.next = new ListNode(1);

        boolean isPal = isPalindrome(pHead);
        System.out.println("LC 234 (Is Palindrome): " + isPal);
        assert isPal : "LC 234 failed";

        System.out.println("\nAll Java Linked List Cycle tests executed successfully! [OK]");
    }
}
