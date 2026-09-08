import java.util.HashMap;
import java.util.Map;

/**
 * Problem: LRU Cache (LeetCode 146 - Medium / High-Frequency FAANG)
 * 
 * Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
 * 
 * Implement the LRUCache class:
 * - LRUCache(int capacity): Initialize the LRU cache with positive size capacity.
 * - int get(int key): Return the value of the key if the key exists, otherwise return -1.
 * - void put(int key, int value): Update the value of the key if the key exists.
 *   Otherwise, add the key-value pair to the cache. If the number of keys exceeds
 *   the capacity from this operation, evict the least recently used key.
 * 
 * Constraints:
 * - get and put must each run in O(1) average time complexity.
 * 
 * Core Design:
 * - Doubly Linked List (DLL): Maintains the chronological order of access in O(1).
 *   - Head dummy node: Points to the Most Recently Used (MRU) node.
 *   - Tail dummy node: Points to the Least Recently Used (LRU) node.
 * - Hash Map: Maps key -> DLL Node in O(1) lookup time.
 * 
 * Complexity:
 * - Time Complexity: O(1) for both get() and put()
 * - Space Complexity: O(capacity) for Hash Map and DLL Nodes
 */
public class lru_cache {

    static class Node {
        int key;
        int value;
        Node prev;
        Node next;

        public Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> map;
    private final Node head; // Dummy head: MRU is head.next
    private final Node tail; // Dummy tail: LRU is tail.prev

    public lru_cache(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("Capacity must be greater than 0");
        }
        this.capacity = capacity;
        this.map = new HashMap<>(capacity);
        this.head = new Node(-1, -1);
        this.tail = new Node(-1, -1);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) {
            return -1;
        }
        Node node = map.get(key);
        // Move accessed node to head (Most Recently Used)
        moveToHead(node);
        return node.value;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.value = value;
            moveToHead(node);
        } else {
            Node newNode = new Node(key, value);
            map.put(key, newNode);
            addNode(newNode);

            if (map.size() > capacity) {
                // Evict LRU node (node right before dummy tail)
                Node lruNode = popTail();
                map.remove(lruNode.key);
            }
        }
    }

    // --- DLL Helper Methods ---

    private void addNode(Node node) {
        // Insert node right after dummy head (MRU position)
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void removeNode(Node node) {
        // Unlink node from its current position
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void moveToHead(Node node) {
        removeNode(node);
        addNode(node);
    }

    private Node popTail() {
        Node lru = tail.prev;
        removeNode(lru);
        return lru;
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 146: LRU Cache (Java)");
        System.out.println("=================================================");

        lru_cache cache = new lru_cache(2);

        cache.put(1, 1);
        cache.put(2, 2);
        System.out.println("get(1) -> expected 1: " + cache.get(1)); // returns 1
        assert cache.get(1) == 1 : "Failed get(1)";

        cache.put(3, 3); // evicts key 2 (key 1 was accessed, so key 2 is LRU)
        System.out.println("get(2) -> expected -1 (evicted): " + cache.get(2)); // returns -1
        assert cache.get(2) == -1 : "Failed eviction check for key 2";

        cache.put(4, 4); // evicts key 1
        System.out.println("get(1) -> expected -1 (evicted): " + cache.get(1));
        assert cache.get(1) == -1 : "Failed eviction check for key 1";

        System.out.println("get(3) -> expected 3: " + cache.get(3));
        assert cache.get(3) == 3 : "Failed get(3)";

        System.out.println("get(4) -> expected 4: " + cache.get(4));
        assert cache.get(4) == 4 : "Failed get(4)";

        // Test updating existing key
        cache.put(4, 40);
        System.out.println("get(4) after update -> expected 40: " + cache.get(4));
        assert cache.get(4) == 40 : "Failed update for key 4";

        System.out.println("\n✅ All LRU Cache tests passed successfully!");
    }
}
