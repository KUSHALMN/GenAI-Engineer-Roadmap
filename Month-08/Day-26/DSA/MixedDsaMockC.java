package Month_08.Day_26.DSA;

import java.util.HashMap;
import java.util.Map;

/**
 * Day 26: Timed DSA Problem Set — Mixed Hard Mock Set C.
 * Focus: LeetCode 146 (LRU Cache) - O(1) Get and Put using Doubly Linked List + HashMap.
 */
public class MixedDsaMockC {

    public static class LRUCache {
        private static class Node {
            int key, val;
            Node prev, next;
            Node(int k, int v) { this.key = k; this.val = v; }
        }

        private final int capacity;
        private final Map<Integer, Node> map;
        private final Node head, tail;

        public LRUCache(int capacity) {
            this.capacity = capacity;
            this.map = new HashMap<>();
            this.head = new Node(0, 0);
            this.tail = new Node(0, 0);
            head.next = tail;
            tail.prev = head;
        }

        public int get(int key) {
            if (!map.containsKey(key)) return -1;
            Node node = map.get(key);
            moveToHead(node);
            return node.val;
        }

        public void put(int key, int value) {
            if (map.containsKey(key)) {
                Node node = map.get(key);
                node.val = value;
                moveToHead(node);
            } else {
                if (map.size() >= capacity) {
                    Node lru = tail.prev;
                    removeNode(lru);
                    map.remove(lru.key);
                }
                Node newNode = new Node(key, value);
                map.put(key, newNode);
                addFirst(newNode);
            }
        }

        private void addFirst(Node node) {
            node.next = head.next;
            node.prev = head;
            head.next.prev = node;
            head.next = node;
        }

        private void removeNode(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }

        private void moveToHead(Node node) {
            removeNode(node);
            addFirst(node);
        }
    }

    public static void main(String[] args) {
        LRUCache lru = new LRUCache(2);
        lru.put(1, 1);
        lru.put(2, 2);
        assert lru.get(1) == 1 : "Get 1 failed";
        lru.put(3, 3); // evicts key 2
        assert lru.get(2) == -1 : "Key 2 should be evicted";
        lru.put(4, 4); // evicts key 1
        assert lru.get(1) == -1 : "Key 1 should be evicted";
        assert lru.get(3) == 3 : "Get 3 failed";
        assert lru.get(4) == 4 : "Get 4 failed";

        System.out.println("Day 26 Mixed Hard Mock Set C (LRU Cache) verification passed.");
    }
}
