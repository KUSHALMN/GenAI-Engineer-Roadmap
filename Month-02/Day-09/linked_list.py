"""
Singly Linked List Operations (Python).
Problems Implemented:
1. Reverse Linked List (LC 206) - O(N) time, O(1) space
2. Linked List Cycle (LC 141) - Floyd's Tortoise and Hare, O(N) time, O(1) space
3. Merge Two Sorted Lists (LC 21) - O(N + M) time, O(1) space
4. Remove Nth Node From End of List (LC 19) - One-pass Two Pointers, O(N) time
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

    @classmethod
    def from_list(cls, elements: List[int]) -> Optional["ListNode"]:
        """Helper to build list from array."""
        dummy = ListNode(0)
        curr = dummy
        for val in elements:
            curr.next = ListNode(val)
            curr = curr.next
        return dummy.next

    def to_list(self) -> List[int]:
        """Convert linked list to Python list."""
        result = []
        curr = self
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result


class LinkedListOperations:

    @staticmethod
    def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
        """LC 206: Reverse Linked List."""
        prev = None
        curr = head
        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        return prev

    @staticmethod
    def has_cycle(head: Optional[ListNode]) -> bool:
        """LC 141: Detect cycle using slow and fast pointers."""
        if not head or not head.next:
            return False

        slow = head
        fast = head.next

        while slow != fast:
            if not fast or not fast.next:
                return False
            slow = slow.next
            fast = fast.next.next

        return True

    @staticmethod
    def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """LC 21: Merge Two Sorted Lists."""
        dummy = ListNode(0)
        curr = dummy

        while l1 and l2:
            if l1.val <= l2.val:
                curr.next = l1
                l1 = l1.next
            else:
                curr.next = l2
                l2 = l2.next
            curr = curr.next

        curr.next = l1 if l1 else l2
        return dummy.next

    @staticmethod
    def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """LC 19: Remove Nth Node From End of List."""
        dummy = ListNode(0, head)
        first = dummy
        second = dummy

        # Advances first pointer so that the gap between first and second is n nodes
        for _ in range(n + 1):
            if first:
                first = first.next

        # Move first to the end, maintaining the gap
        while first:
            first = first.next
            second = second.next

        if second and second.next:
            second.next = second.next.next

        return dummy.next


if __name__ == "__main__":
    ops = LinkedListOperations()

    # LC 206 Reverse
    ll1 = ListNode.from_list([1, 2, 3, 4, 5])
    rev = ops.reverse_list(ll1)
    assert rev.to_list() == [5, 4, 3, 2, 1]

    # LC 21 Merge
    a = ListNode.from_list([1, 2, 4])
    b = ListNode.from_list([1, 3, 4])
    merged = ops.merge_two_lists(a, b)
    assert merged.to_list() == [1, 1, 2, 3, 4, 4]

    # LC 19 Remove Nth
    ll2 = ListNode.from_list([1, 2, 3, 4, 5])
    rem = ops.remove_nth_from_end(ll2, 2)
    assert rem.to_list() == [1, 2, 3, 5]

    # LC 141 Cycle
    c1 = ListNode(1)
    c2 = ListNode(2)
    c1.next = c2
    c2.next = c1  # cycle
    assert ops.has_cycle(c1) is True

    c3 = ListNode.from_list([1, 2, 3])
    assert ops.has_cycle(c3) is False

    print("All Linked List Python tests passed successfully!")
