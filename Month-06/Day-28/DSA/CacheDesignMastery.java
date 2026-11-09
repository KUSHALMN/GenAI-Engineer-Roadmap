import java.util.*;

public class CacheDesignMastery {
    // LC 146: LRU Cache implementation with Doubly Linked List + HashMap
    public static class LRUCache {
        static class Node {
            int key, val;
            Node prev, next;
            Node(int k, int v) { key = k; val = v; }
        }

        private final int capacity;
        private final Map<Integer, Node> map = new HashMap<>();
        private final Node head = new Node(0, 0);
        private final Node tail = new Node(0, 0);

        public LRUCache(int capacity) {
            this.capacity = capacity;
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
            }
            if (map.size() >= capacity) {
                map.remove(tail.prev.key);
                remove(tail.prev);
            }
            Node node = new Node(key, value);
            insertHead(node);
            map.put(key, node);
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
    }

    public static void main(String[] args) {
        System.out.println("=== Cache Design Mastery Verification ===");
        LRUCache lru = new LRUCache(2);
        lru.put(1, 1);
        lru.put(2, 2);
        assert lru.get(1) == 1 : "Expected 1";
        lru.put(3, 3); // Evicts key 2
        assert lru.get(2) == -1 : "Expected -1 (evicted)";
        lru.put(4, 4); // Evicts key 1
        assert lru.get(1) == -1 : "Expected -1 (evicted)";
        assert lru.get(3) == 3 : "Expected 3";
        assert lru.get(4) == 4 : "Expected 4";
        System.out.println("LRU Cache O(1) operations passed successfully!");
    }
}
