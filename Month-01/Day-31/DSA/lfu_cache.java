import java.util.*;

/**
 * Problem: LFU Cache (LeetCode 460 - Hard / Legendary FAANG System Design Problem)
 * 
 * Design and implement a data structure for a Least Frequently Used (LFU) cache.
 * 
 * Implement the LFUCache class:
 * - LFUCache(int capacity): Initializes the object with the capacity of the data structure.
 * - int get(int key): Gets the value of the key if it exists in the cache, otherwise -1.
 * - void put(int key, int value): Update or insert value. When cache reaches capacity,
 *   invalidate and remove the least frequently used key. If tie, evict the least recently used key.
 * 
 * Both functions MUST run in O(1) average time complexity.
 * 
 * Optimal Architecture:
 * - Map<Integer, Node> keyMap: Maps key -> Node.
 * - Map<Integer, DoublyLinkedList> freqMap: Maps frequency -> DoublyLinkedList of nodes with that frequency.
 * - int minFreq: Tracks the global minimum frequency across the cache.
 * 
 * Complexity:
 * - Time: O(1) strictly for get() and put()
 * - Space: O(capacity) for HashMap and DLL nodes
 */
public class lfu_cache {

    static class Node {
        int key;
        int value;
        int freq;
        Node prev;
        Node next;

        Node(int key, int value) {
            this.key = key;
            this.value = value;
            this.freq = 1;
        }
    }

    static class DoublyLinkedList {
        Node head;
        Node tail;
        int size;

        DoublyLinkedList() {
            head = new Node(-1, -1);
            tail = new Node(-1, -1);
            head.next = tail;
            tail.prev = head;
            size = 0;
        }

        void addNode(Node node) {
            node.next = head.next;
            node.prev = head;
            head.next.prev = node;
            head.next = node;
            size++;
        }

        void removeNode(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
            size--;
        }

        Node removeTail() {
            if (size == 0) return null;
            Node lru = tail.prev;
            removeNode(lru);
            return lru;
        }
    }

    private final int capacity;
    private int curSize;
    private int minFreq;
    private final Map<Integer, Node> keyMap;
    private final Map<Integer, DoublyLinkedList> freqMap;

    public lfu_cache(int capacity) {
        this.capacity = capacity;
        this.curSize = 0;
        this.minFreq = 0;
        this.keyMap = new HashMap<>();
        this.freqMap = new HashMap<>();
    }

    public int get(int key) {
        Node node = keyMap.get(key);
        if (node == null) return -1;
        updateNode(node);
        return node.value;
    }

    public void put(int key, int value) {
        if (capacity <= 0) return;

        if (keyMap.containsKey(key)) {
            Node node = keyMap.get(key);
            node.value = value;
            updateNode(node);
        } else {
            curSize++;
            if (curSize > capacity) {
                DoublyLinkedList minList = freqMap.get(minFreq);
                Node toDelete = minList.removeTail();
                keyMap.remove(toDelete.key);
                curSize--;
            }

            minFreq = 1;
            Node newNode = new Node(key, value);
            keyMap.put(key, newNode);

            DoublyLinkedList curList = freqMap.computeIfAbsent(1, k -> new DoublyLinkedList());
            curList.addNode(newNode);
        }
    }

    private void updateNode(Node node) {
        int curFreq = node.freq;
        DoublyLinkedList curList = freqMap.get(curFreq);
        curList.removeNode(node);

        if (curFreq == minFreq && curList.size == 0) {
            minFreq++;
        }

        node.freq++;
        DoublyLinkedList nextList = freqMap.computeIfAbsent(node.freq, k -> new DoublyLinkedList());
        nextList.addNode(node);
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 460: LFU Cache (Java O(1))");
        System.out.println("=================================================");

        lfu_cache lfu = new lfu_cache(2);

        lfu.put(1, 1);
        lfu.put(2, 2);
        System.out.println("get(1) -> Expected 1: " + lfu.get(1)); // returns 1, freq(1)=2
        assert lfu.get(1) == 1 : "Failed get(1)";

        lfu.put(3, 3); // evicts key 2 (freq(2)=1, freq(1)=2)
        System.out.println("get(2) after evict -> Expected -1: " + lfu.get(2)); // returns -1
        assert lfu.get(2) == -1 : "Failed eviction of key 2";

        System.out.println("get(3) -> Expected 3: " + lfu.get(3)); // returns 3
        assert lfu.get(3) == 3 : "Failed get(3)";

        lfu.put(4, 4); // evicts key 1 (both 1 and 3 have freq 2, but 1 was accessed least recently!)
        System.out.println("get(1) after tie-breaker evict -> Expected -1: " + lfu.get(1));
        assert lfu.get(1) == -1 : "Failed tie-breaker eviction of key 1";

        System.out.println("get(3) -> Expected 3: " + lfu.get(3));
        assert lfu.get(3) == 3 : "Failed get(3)";

        System.out.println("get(4) -> Expected 4: " + lfu.get(4));
        assert lfu.get(4) == 4 : "Failed get(4)";

        System.out.println("\n✅ All LFU Cache tests passed successfully!");
    }
}
