import java.util.HashMap;

/**
 * LeetCode 146 - LRU Cache
 * Topic: Doubly Linked List + HashMap — O(1) get & put
 *
 * Design: HashMap<key, Node> for O(1) lookup.
 *         Doubly linked list maintains LRU order.
 *         head.next = most recently used
 *         tail.prev = least recently used
 *
 * Time:  O(1) get and put
 * Space: O(capacity)
 */
public class LRUCache {

    private static class Node {
        int key, val;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }

    private final int capacity;
    private final HashMap<Integer, Node> map;
    private final Node head, tail; // sentinels

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.map = new HashMap<>();
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node node = map.get(key);
        moveToFront(node);
        return node.val;
    }

    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.val = value;
            moveToFront(node);
        } else {
            if (map.size() == capacity) {
                Node lru = tail.prev;
                remove(lru);
                map.remove(lru.key);
            }
            Node node = new Node(key, value);
            insertFront(node);
            map.put(key, node);
        }
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertFront(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }

    private void moveToFront(Node node) {
        remove(node);
        insertFront(node);
    }

    public static void main(String[] args) {
        LRUCache cache = new LRUCache(2);
        cache.put(1, 1);
        cache.put(2, 2);
        System.out.println(cache.get(1));   // 1
        cache.put(3, 3);                    // evicts key 2
        System.out.println(cache.get(2));   // -1
        cache.put(4, 4);                    // evicts key 1
        System.out.println(cache.get(1));   // -1
        System.out.println(cache.get(3));   // 3
        System.out.println(cache.get(4));   // 4
    }
}
