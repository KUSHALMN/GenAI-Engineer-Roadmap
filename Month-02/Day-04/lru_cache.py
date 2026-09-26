"""
LRU Cache & HashMap Frequency Counting implemented from scratch.
No functools.lru_cache or collections.OrderedDict used.
"""

from typing import Any, Dict, List, Optional, Tuple


class Node:
    """Doubly Linked List Node for LRU Cache."""

    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class LRUCache:
    """
    Least Recently Used (LRU) Cache implemented using a HashMap + Doubly Linked List.
    All operations (get, put, remove) operate in O(1) time complexity.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive integer")
        self.capacity = capacity
        self.cache: Dict[Any, Node] = {}

        # Dummy head and tail nodes to avoid edge-case pointer checks
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node_to_head(self, node: Node) -> None:
        """Insert node right after head (most recently used position)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node) -> None:
        """Move existing node to the head of the list."""
        self._remove_node(node)
        self._add_node_to_head(node)

    def _pop_tail(self) -> Node:
        """Pop the least recently used node (node right before tail)."""
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve item by key. Marks item as most recently used."""
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """Insert or update item. If over capacity, evicts LRU item."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node_to_head(new_node)

            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]

    def contains(self, key: Any) -> bool:
        """Check if key exists in cache without updating recency."""
        return key in self.cache

    def size(self) -> int:
        """Current number of items in cache."""
        return len(self.cache)

    def clear(self) -> None:
        """Empty the cache."""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head


class FrequencyCounter:
    """
    HashMap frequency counting utilities for tokens, words, and query terms.
    Provides top-k most frequent items in O(N log K) time.
    """

    def __init__(self):
        self.counts: Dict[str, int] = {}

    def add(self, item: str, amount: int = 1) -> None:
        """Increment count for an item."""
        self.counts[item] = self.counts.get(item, 0) + amount

    def add_batch(self, items: List[str]) -> None:
        """Count multiple items."""
        for item in items:
            self.add(item)

    def get_count(self, item: str) -> int:
        """Get frequency of an item."""
        return self.counts.get(item, 0)

    def top_k(self, k: int) -> List[Tuple[str, int]]:
        """Return the top-k most frequent items sorted descending."""
        sorted_items = sorted(self.counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:k]

    def total_items(self) -> int:
        """Total number of counted instances."""
        return sum(self.counts.values())

    def unique_items(self) -> int:
        """Total distinct items."""
        return len(self.counts)


if __name__ == "__main__":
    # Self-test LRU Cache
    cache = LRUCache(capacity=2)
    cache.put("q1", "Answer 1")
    cache.put("q2", "Answer 2")
    assert cache.get("q1") == "Answer 1"
    cache.put("q3", "Answer 3")  # Evicts q2
    assert cache.get("q2") is None
    assert cache.get("q3") == "Answer 3"
    print("LRUCache tests passed successfully!")

    # Self-test FrequencyCounter
    fc = FrequencyCounter()
    fc.add_batch(["llama", "gpt4", "claude", "llama", "llama", "gpt4"])
    assert fc.get_count("llama") == 3
    assert fc.top_k(2) == [("llama", 3), ("gpt4", 2)]
    print("FrequencyCounter tests passed successfully!")
