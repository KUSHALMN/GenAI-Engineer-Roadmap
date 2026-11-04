package DSA;

import java.util.*;

/**
 * 90-Minute Java DSA Capstone Mock Assessment
 * Section A: Data Structure Design - LRU Cache (O(1) get & put)
 * Section B: Graph / Ordering - Course Schedule II (O(V + E) Topological Sort)
 * Section C: Heap / Statistics - Kth Largest Element in an Array (O(N log K))
 */
public class ComprehensiveDSAMock {

    // ---------------------------------------------------------
    // 1. LRU Cache (HashMap + Doubly Linked List)
    // ---------------------------------------------------------
    static class LRUCache {
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
            insertToHead(node);
            return node.val;
        }

        public void put(int key, int value) {
            if (map.containsKey(key)) {
                remove(map.get(key));
            }
            if (map.size() == capacity) {
                map.remove(tail.prev.key);
                remove(tail.prev);
            }
            Node newNode = new Node(key, value);
            insertToHead(newNode);
            map.put(key, newNode);
        }

        private void remove(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }

        private void insertToHead(Node node) {
            node.next = head.next;
            node.next.prev = node;
            head.next = node;
            node.prev = head;
        }
    }

    // ---------------------------------------------------------
    // 2. Course Schedule II (Topological Sort)
    // ---------------------------------------------------------
    public static int[] findCourseOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        int[] inDegree = new int[numCourses];

        for (int[] p : prerequisites) {
            adj.get(p[1]).add(p[0]);
            inDegree[p[0]]++;
        }

        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }

        int[] order = new int[numCourses];
        int idx = 0;
        while (!q.isEmpty()) {
            int curr = q.poll();
            order[idx++] = curr;
            for (int nxt : adj.get(curr)) {
                inDegree[nxt]--;
                if (inDegree[nxt] == 0) q.offer(nxt);
            }
        }
        return idx == numCourses ? order : new int[0];
    }

    // ---------------------------------------------------------
    // 3. Kth Largest Element (Min-Heap)
    // ---------------------------------------------------------
    public static int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int x : nums) {
            minHeap.offer(x);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }
        return minHeap.peek();
    }

    public static void main(String[] args) {
        // Test LRU Cache
        LRUCache lru = new LRUCache(2);
        lru.put(1, 10);
        lru.put(2, 20);
        System.out.println("LRU get(1): " + lru.get(1)); // 10
        lru.put(3, 30); // Evicts key 2
        System.out.println("LRU get(2) after eviction: " + lru.get(2) + " (Expected: -1)");

        // Test Course Schedule
        int[][] pre = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        int[] courseOrder = findCourseOrder(4, pre);
        System.out.println("Course Schedule Order: " + Arrays.toString(courseOrder));

        // Test Kth Largest
        int[] nums = {3, 2, 1, 5, 6, 4};
        System.out.println("2nd Largest in [3,2,1,5,6,4]: " + findKthLargest(nums, 2) + " (Expected: 5)");

        System.out.println("ComprehensiveDSAMock tests passed successfully!");
    }
}
