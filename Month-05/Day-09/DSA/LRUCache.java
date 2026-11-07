import java.util.*;

/**
 * Day 09: Advanced Design — LRU Cache
 * Implements Least Recently Used cache with O(1) get and put
 * using HashMap + Custom Doubly Linked List.
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
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node n = map.get(key);
        remove(n);
        insertHead(n);
        return n.val;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            remove(map.get(key));
        } else if (map.size() == capacity) {
            map.remove(tail.prev.key);
            remove(tail.prev);
        }
        Node n = new Node(key, value);
        insertHead(n);
        map.put(key, n);
    }

    private void remove(Node n) {
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }

    private void insertHead(Node n) {
        n.next = head.next;
        n.next.prev = n;
        head.next = n;
        n.prev = head;
    }

    public static void main(String[] args) {
        LRUCache lru = new LRUCache(2);
        lru.put(1, 10);
        lru.put(2, 20);
        assert lru.get(1) == 10;
        lru.put(3, 30); // Evicts key 2
        assert lru.get(2) == -1;
        assert lru.get(3) == 30;
        System.out.println("Day 09 DSA LRUCache verification passed!");
    }
}
