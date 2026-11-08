/**
 * Fast & Slow Pointers Revision Patterns
 * Solves core FAANG interview problems:
 * 1. Linked List Cycle I (LC 141)
 * 2. Linked List Cycle II (LC 142) - Find Cycle Start
 * 3. Happy Number (LC 202)
 * 4. Middle of the Linked List (LC 876)
 */

public class FastSlowPointersRevision {

    public static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    // 1. LC 141: Cycle Detection
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

    // 2. LC 142: Find Cycle Start Node
    public static ListNode detectCycle(ListNode head) {
        if (head == null || head.next == null) return null;
        ListNode slow = head;
        ListNode fast = head;
        boolean hasCycle = false;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                hasCycle = true;
                break;
            }
        }

        if (!hasCycle) return null;

        ListNode ptr1 = head;
        ListNode ptr2 = slow;
        while (ptr1 != ptr2) {
            ptr1 = ptr1.next;
            ptr2 = ptr2.next;
        }
        return ptr1;
    }

    // 3. LC 202: Happy Number
    public static boolean isHappy(int n) {
        int slow = n;
        int fast = getNextSum(n);
        while (fast != 1 && slow != fast) {
            slow = getNextSum(slow);
            fast = getNextSum(getNextSum(fast));
        }
        return fast == 1;
    }

    private static int getNextSum(int n) {
        int sum = 0;
        while (n > 0) {
            int d = n % 10;
            sum += d * d;
            n /= 10;
        }
        return sum;
    }

    // 4. LC 876: Middle of Linked List
    public static ListNode middleNode(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    public static void main(String[] args) {
        System.out.println("=== Fast & Slow Pointers Verification ===");

        // Test LC 141 & 142
        ListNode n1 = new ListNode(3);
        ListNode n2 = new ListNode(2);
        ListNode n3 = new ListNode(0);
        ListNode n4 = new ListNode(-4);
        n1.next = n2; n2.next = n3; n3.next = n4; n4.next = n2; // Cycle at n2

        assert hasCycle(n1) : "LC 141 failed";
        ListNode cycleStart = detectCycle(n1);
        System.out.println("LC 142: Cycle starts at node with val " + cycleStart.val);
        assert cycleStart == n2 : "LC 142 failed";

        // Test LC 202
        assert isHappy(19) : "LC 202 failed for 19";
        assert !isHappy(2) : "LC 202 failed for 2";
        System.out.println("LC 202 (Happy Number): 19 is happy, 2 is not");

        System.out.println("All Fast/Slow pointer tests passed successfully!");
    }
}
