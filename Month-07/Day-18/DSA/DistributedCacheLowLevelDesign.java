package Month07.Day18;

import java.util.HashMap;
import java.util.Map;

/**
 * Low-Level Design (LLD): In-Memory Distributed Cache Node
 * Implements O(1) LRU eviction policy with doubly linked list + hash map.
 */
public class DistributedCacheLowLevelDesign {

    public static class LRUCache<K, V> {
        private static class Node<K, V> {
            K key;
            V value;
            Node<K, V> prev, next;
            Node(K k, V v) { this.key = k; this.value = v; }
        }

        private final int capacity;
        private final Map<K, Node<K, V>> map = new HashMap<>();
        private final Node<K, V> head = new Node<>(null, null);
        private final Node<K, V> tail = new Node<>(null, null);

        public LRUCache(int capacity) {
            this.capacity = capacity;
            head.next = tail;
            tail.prev = head;
        }

        private void remove(Node<K, V> node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }

        private void insertAtFront(Node<K, V> node) {
            node.next = head.next;
            node.prev = head;
            head.next.prev = node;
            head.next = node;
        }

        public synchronized V get(K key) {
            Node<K, V> node = map.get(key);
            if (node == null) return null;
            remove(node);
            insertAtFront(node);
            return node.value;
        }

        public synchronized void put(K key, V value) {
            if (map.containsKey(key)) {
                remove(map.get(key));
            }
            if (map.size() == capacity) {
                map.remove(tail.prev.key);
                remove(tail.prev);
            }
            Node<K, V> newNode = new Node<>(key, value);
            map.put(key, newNode);
            insertAtFront(newNode);
        }
    }

    public static void main(String[] args) {
        LRUCache<String, String> cache = new LRUCache<>(2);
        cache.put("k1", "v1");
        cache.put("k2", "v2");
        assert cache.get("k1").equals("v1");

        cache.put("k3", "v3"); // Evicts k2!
        assert cache.get("k2") == null;
        assert cache.get("k3").equals("v3");

        System.out.println("Day 18 Distributed Cache LLD verification passed.");
    }
}
