# 💻 Day 23 Coding Interview Questions: LRU Cache & Async Streaming

### Problem: Design and Implement LRU Cache (LeetCode 146 - Medium / High-Frequency)
**Key Insight**:
To achieve strictly $O(1)$ time for both `get` and `put`, we need two components:
1. A **HashMap** providing $O(1)$ search from key to memory location.
2. A **Doubly Linked List (DLL)** where nodes can be spliced and moved to the head (most recently used) or evicted from the tail (least recently used) in $O(1)$ without scanning array indices.

```java
// Splicing a node in O(1):
private void removeNode(Node node) {
    node.prev.next = node.next;
    node.next.prev = node.prev;
}

private void addNode(Node node) {
    node.prev = head;
    node.next = head.next;
    head.next.prev = node;
    head.next = node;
}
```

**Common Interview Follow-ups**:
- *How would you make this thread-safe in Java?* Use `ConcurrentHashMap` with `ReentrantReadWriteLock` or synchronization over DLL mutations.
- *How does LRU differ from LFU?* LRU tracks recency of last access; LFU tracks total frequency count across time.
