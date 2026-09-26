import java.util.HashMap;
import java.util.Map;

/**
 * LeetCode 146 - LRU Cache
 * Topic: Hash Table, Doubly-Linked List, Design
 *
 * Problem: Design a data structure that follows the constraints of a
 * Least Recently Used (LRU) cache. Implement get(key) and put(key, value) in O(1).
 *
 * Approach:
 *   - Use a HashMap<Integer, Node> for O(1) key-to-node lookup.
 *   - Use a Doubly Linked List with dummy head and tail to maintain access order in O(1).
 *   - Most recently used nodes are placed near head.
 *   - Least recently used nodes are near tail.
 *
 * Time Complexity:  O(1) for both get and put
 * Space Complexity: O(capacity)
 */
public class LRUCache {

    private static class Node {
        int key;
        int value;
        Node prev;
        Node next;

        Node() {}
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> cache;
    private final Node head;
    private final Node tail;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        this.head = new Node();
        this.tail = new Node();
        head.next = tail;
        tail.prev = head;
    }

    private void addNode(Node node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void removeNode(Node node) {
        Node prevNode = node.prev;
        Node nextNode = node.next;
        prevNode.next = nextNode;
        nextNode.prev = prevNode;
    }

    private void moveToHead(Node node) {
        removeNode(node);
        addNode(node);
    }

    private Node popTail() {
        Node res = tail.prev;
        removeNode(res);
        return res;
    }

    public int get(int key) {
        Node node = cache.get(key);
        if (node == null) {
            return -1;
        }
        moveToHead(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node node = cache.get(key);
        if (node != null) {
            node.value = value;
            moveToHead(node);
        } else {
            Node newNode = new Node(key, value);
            cache.put(key, newNode);
            addNode(newNode);

            if (cache.size() > capacity) {
                Node tailNode = popTail();
                cache.remove(tailNode.key);
            }
        }
    }

    public static void main(String[] args) {
        LRUCache lru = new LRUCache(2);

        lru.put(1, 1); // cache is {1=1}
        lru.put(2, 2); // cache is {1=1, 2=2}
        System.out.println("get(1): " + lru.get(1)); // return 1

        lru.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
        System.out.println("get(2): " + lru.get(2)); // return -1 (not found)

        lru.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
        System.out.println("get(1): " + lru.get(1)); // return -1 (not found)
        System.out.println("get(3): " + lru.get(3)); // return 3
        System.out.println("get(4): " + lru.get(4)); // return 4
    }
}
