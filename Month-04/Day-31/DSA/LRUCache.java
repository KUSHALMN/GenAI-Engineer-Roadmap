import java.util.*;

/**
 * Day 31: Advanced Design — LRU Cache
 * Problem: Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
 * Functions: get(key) and put(key, value) in O(1) time complexity.
 *
 * Algorithm:
 * - HashMap<Integer, Node> for O(1) lookup.
 * - Custom Doubly Linked List with dummy head and tail for O(1) node addition and removal.
 *
 * Time Complexity: O(1) for both get() and put()
 * Space Complexity: O(capacity)
 */
public class LRUCache {

    static class Node {
        int key, val;
        Node prev, next;
        Node(int key, int val) { this.key = key; this.val = val; }
    }

    private final int capacity;
    private final Map<Integer, Node> map;
    private final Node head, tail;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.map = new HashMap<>();
        this.head = new Node(-1, -1);
        this.tail = new Node(-1, -1);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        remove(node);
        insertHead(node);
        return node.val;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            remove(map.get(key));
        } else if (map.size() == capacity) {
            map.remove(tail.prev.key);
            remove(tail.prev);
        }
        Node newNode = new Node(key, value);
        insertHead(newNode);
        map.put(key, newNode);
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertHead(Node node) {
        node.next = head.next;
        node.next.prev = node;
        head.next = node;
        node.prev = head;
    }

    public static void main(String[] args) {
        LRUCache lru = new LRUCache(2);
        lru.put(1, 1);
        lru.put(2, 2);
        assert lru.get(1) == 1; // returns 1
        lru.put(3, 3);          // evicts key 2
        assert lru.get(2) == -1; // returns -1 (not found)
        lru.put(4, 4);          // evicts key 1
        assert lru.get(1) == -1; // returns -1
        assert lru.get(3) == 3;  // returns 3
        assert lru.get(4) == 4;  // returns 4

        System.out.println("Day 31 DSA LRUCache verification passed!");
    }
}
