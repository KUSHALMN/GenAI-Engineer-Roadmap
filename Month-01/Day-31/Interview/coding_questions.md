# 💻 Day 31 Coding Interview Questions: LFU Cache (LeetCode 460 - Hard)

### Problem: Design and Implement LFU Cache (LeetCode 460 - Hard / Legendary FAANG)
**Key Insight (O(1) Strictly for Get and Put)**:
To achieve $O(1)$ operations on both access and eviction:
1. Maintain `keyMap`: maps `key` to `Node`.
2. Maintain `freqMap`: maps `frequency` to a `DoublyLinkedList` of nodes having that exact frequency.
3. Track `minFreq`: the minimum frequency present across the entire cache.

```java
// When a node is accessed:
int curFreq = node.freq;
DoublyLinkedList curList = freqMap.get(curFreq);
curList.removeNode(node);

if (curFreq == minFreq && curList.size == 0) {
    minFreq++;
}

node.freq++;
DoublyLinkedList nextList = freqMap.computeIfAbsent(node.freq, k -> new DoublyLinkedList());
nextList.addNode(node);
```

**Tie-Breaking Condition**:
When multiple keys have the same minimum frequency, the `DoublyLinkedList` for that frequency naturally keeps items ordered chronologically, so removing from the tail evicts the *least recently used* node among the least frequently used keys in $O(1)$ time.
