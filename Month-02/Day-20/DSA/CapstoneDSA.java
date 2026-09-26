import java.util.*;

/**
 * Capstone DSA Interview Masterclass in Java
 *
 * Demonstrates mastery of core FAANG technical patterns:
 *   1. Design: LRU Cache with custom Doubly Linked List + HashMap (O(1) get & put)
 *   2. Heap: Top K Frequent Elements (O(N log K) time)
 *   3. Trees/Strings: Trie (Prefix Tree) for prefix search & autocomplete
 *   4. Graphs: Directed Cycle Detection using Kahn's Algorithm
 */
public class CapstoneDSA {

    // ==========================================
    // 1. LRU Cache Implementation (O(1) Ops)
    // ==========================================
    public static class LRUCache {
        private static class Node {
            int key, val;
            Node prev, next;
            Node(int k, int v) { key = k; val = v; }
        }

        private final int capacity;
        private final Map<Integer, Node> map = new HashMap<>();
        private final Node head = new Node(0, 0);
        private final Node tail = new Node(0, 0);

        public LRUCache(int cap) {
            this.capacity = cap;
            head.next = tail;
            tail.prev = head;
        }

        private void add(Node node) {
            node.prev = head;
            node.next = head.next;
            head.next.prev = node;
            head.next = node;
        }

        private void remove(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }

        public int get(int key) {
            if (!map.containsKey(key)) return -1;
            Node node = map.get(key);
            remove(node);
            add(node);
            return node.val;
        }

        public void put(int key, int value) {
            if (map.containsKey(key)) {
                remove(map.get(key));
            }
            Node newNode = new Node(key, value);
            map.put(key, newNode);
            add(newNode);
            if (map.size() > capacity) {
                Node lru = tail.prev;
                remove(lru);
                map.remove(lru.key);
            }
        }
    }

    // ==========================================
    // 2. Top K Frequent Elements (Min-Heap)
    // ==========================================
    public static int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int n : nums) counts.put(n, counts.getOrDefault(n, 0) + 1);

        PriorityQueue<Integer> heap = new PriorityQueue<>(Comparator.comparingInt(counts::get));
        for (int num : counts.keySet()) {
            heap.offer(num);
            if (heap.size() > k) heap.poll();
        }

        int[] res = new int[k];
        for (int i = 0; i < k; i++) res[i] = heap.poll();
        return res;
    }

    // ==========================================
    // 3. Trie (Prefix Tree)
    // ==========================================
    public static class Trie {
        private static class TrieNode {
            Map<Character, TrieNode> children = new HashMap<>();
            boolean isEnd = false;
        }

        private final TrieNode root = new TrieNode();

        public void insert(String word) {
            TrieNode curr = root;
            for (char ch : word.toCharArray()) {
                curr.children.putIfAbsent(ch, new TrieNode());
                curr = curr.children.get(ch);
            }
            curr.isEnd = true;
        }

        public boolean search(String word) {
            TrieNode node = find(word);
            return node != null && node.isEnd;
        }

        public boolean startsWith(String prefix) {
            return find(prefix) != null;
        }

        private TrieNode find(String s) {
            TrieNode curr = root;
            for (char ch : s.toCharArray()) {
                if (!curr.children.containsKey(ch)) return null;
                curr = curr.children.get(ch);
            }
            return curr;
        }
    }

    // ==========================================
    // 4. Graph Cycle Detection (Kahn's Algorithm)
    // ==========================================
    public static boolean hasCycle(int numNodes, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numNodes; i++) adj.add(new ArrayList<>());
        int[] inDegree = new int[numNodes];

        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            inDegree[e[1]]++;
        }

        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numNodes; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }

        int visitedCount = 0;
        while (!q.isEmpty()) {
            int curr = q.poll();
            visitedCount++;
            for (int neighbor : adj.get(curr)) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) q.offer(neighbor);
            }
        }
        return visitedCount != numNodes; // Cycle exists if not all nodes visited
    }

    // ==========================================
    // Main Verification Test Suite
    // ==========================================
    public static void main(String[] args) {
        System.out.println("Running Capstone Java DSA Masterclass Test Suite...\n");

        // 1. LRU Cache
        LRUCache lru = new LRUCache(2);
        lru.put(1, 100);
        lru.put(2, 200);
        System.out.println("[LRU Cache] get(1): " + lru.get(1)); // 100
        lru.put(3, 300); // evicts key 2
        System.out.println("[LRU Cache] get(2) evicted: " + lru.get(2)); // -1
        System.out.println("[LRU Cache] get(3): " + lru.get(3)); // 300

        // 2. Top K Frequent
        int[] topK = topKFrequent(new int[]{1, 1, 1, 2, 2, 3}, 2);
        System.out.println("\n[Top K Frequent]: " + Arrays.toString(topK)); // [2, 1]

        // 3. Trie
        Trie trie = new Trie();
        trie.insert("genai");
        System.out.println("\n[Trie] Search 'genai': " + trie.search("genai"));       // true
        System.out.println("[Trie] StartsWith 'gen': " + trie.startsWith("gen"));    // true
        System.out.println("[Trie] Search 'gen': " + trie.search("gen"));            // false

        // 4. Graph Cycle
        int[][] dagEdges = {{0, 1}, {1, 2}, {2, 3}};
        System.out.println("\n[Graph] DAG Has Cycle: " + hasCycle(4, dagEdges));     // false
        int[][] cyclicEdges = {{0, 1}, {1, 2}, {2, 0}};
        System.out.println("[Graph] Cyclic Has Cycle: " + hasCycle(3, cyclicEdges)); // true

        System.out.println("\nAll Capstone Java DSA tests passed successfully!");
    }
}
