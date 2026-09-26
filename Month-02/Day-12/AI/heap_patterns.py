"""
Heap & Priority Queue Patterns (Python).
Problems Implemented:
1. Kth Largest Element in an Array (LC 215) - Min-Heap, O(N log K) time, O(K) space
2. Top K Frequent Elements (LC 347) - Min-Heap, O(N log K) time, O(N) space
3. Merge K Sorted Lists (LC 23) - Min-Heap, O(N log K) time, O(K) space
4. Find Median from Data Stream (LC 295) - Two Heaps (Max-Heap + Min-Heap)
"""

import heapq
from typing import Dict, List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

    # Needed for heapq comparison tie-breaking
    def __lt__(self, other: "ListNode") -> bool:
        return self.val < other.val


class HeapPatterns:

    @staticmethod
    def find_kth_largest(nums: List[int], k: int) -> int:
        """LC 215: Kth Largest Element using a Min-Heap of size k."""
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]

    @staticmethod
    def top_k_frequent(nums: List[int], k: int) -> List[int]:
        """LC 347: Top K Frequent Elements."""
        counts: Dict[int, int] = {}
        for n in nums:
            counts[n] = counts.get(n, 0) + 1

        # Min-heap of tuples (frequency, num)
        heap = []
        for num, freq in counts.items():
            heapq.heappush(heap, (freq, num))
            if len(heap) > k:
                heapq.heappop(heap)

        return [num for freq, num in heap]

    @staticmethod
    def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """LC 23: Merge K Sorted Lists."""
        heap = []
        for i, l in enumerate(lists):
            if l:
                heapq.heappush(heap, (l.val, i, l))

        dummy = ListNode(0)
        curr = dummy

        while heap:
            val, i, node = heapq.heappop(heap)
            curr.next = node
            curr = curr.next

            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))

        return dummy.next


class MedianFinder:
    """LC 295: Find Median from Data Stream using Two Heaps."""

    def __init__(self):
        # max_heap for lower half (store negative for Python min-heap)
        self.small = []
        # min_heap for upper half
        self.large = []

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)

        # Ensure every element in small <= large
        if self.small and self.large and (-self.small[0]) > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance sizes (small can have at most 1 more element than large)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


if __name__ == "__main__":
    hp = HeapPatterns()

    # LC 215
    assert hp.find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert hp.find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

    # LC 347
    top2 = hp.top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    assert set(top2) == {1, 2}

    # LC 295
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2.0

    print("All Heap/Priority Queue Python tests passed successfully!")
