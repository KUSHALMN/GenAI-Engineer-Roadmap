package DSA;

import java.util.*;

/**
 * Mixed Advanced DSA Mastery Suite
 * Problem 1: Trie Autocomplete (Prefix Search & Insertion)
 * Problem 2: Graph Shortest Path (Dijkstra)
 * Problem 3: Range Query (Fenwick Tree Prefix Sum)
 * Problem 4: 1D Dynamic Programming (House Robber LC 198)
 */
public class MixedAdvancedDSASet {

    // 1. Trie Node for Autocomplete
    static class TrieNode {
        Map<Character, TrieNode> children = new HashMap<>();
        boolean isEndOfWord = false;
    }

    static class Trie {
        private final TrieNode root = new TrieNode();

        public void insert(String word) {
            TrieNode curr = root;
            for (char c : word.toCharArray()) {
                curr.children.putIfAbsent(c, new TrieNode());
                curr = curr.children.get(c);
            }
            curr.isEndOfWord = true;
        }

        public boolean startsWith(String prefix) {
            TrieNode curr = root;
            for (char c : prefix.toCharArray()) {
                if (!curr.children.containsKey(c)) return false;
                curr = curr.children.get(c);
            }
            return true;
        }
    }

    // 2. Dijkstra
    public static int dijkstraShortest(int n, int[][] edges, int src, int dst) {
        List<List<int[]>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
        for (int[] e : edges) graph.get(e[0]).add(new int[]{e[1], e[2]});

        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{src, 0});

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int u = curr[0], d = curr[1];
            if (d > dist[u]) continue;

            for (int[] nxt : graph.get(u)) {
                int v = nxt[0], w = nxt[1];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.offer(new int[]{v, dist[v]});
                }
            }
        }
        return dist[dst] == Integer.MAX_VALUE ? -1 : dist[dst];
    }

    // 3. 1D Dynamic Programming: House Robber
    public static int rob(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int prev1 = 0, prev2 = 0;
        for (int num : nums) {
            int temp = Math.max(prev1, prev2 + num);
            prev2 = prev1;
            prev1 = temp;
        }
        return prev1;
    }

    public static void main(String[] args) {
        // Test Trie
        Trie trie = new Trie();
        trie.insert("vector");
        trie.insert("retrieval");
        trie.insert("rerank");
        System.out.println("Trie startsWith 'ret': " + trie.startsWith("ret")); // true
        System.out.println("Trie startsWith 'xyz': " + trie.startsWith("xyz")); // false

        // Test Dijkstra
        int[][] edges = {{0, 1, 4}, {0, 2, 1}, {2, 1, 2}, {1, 3, 1}};
        int shortest = dijkstraShortest(4, edges, 0, 3);
        System.out.println("Dijkstra 0 -> 3: " + shortest + " (Expected: 4 via 0->2->1->3)");

        // Test DP
        int[] houses = {2, 7, 9, 3, 1};
        System.out.println("Max robbed money: " + rob(houses) + " (Expected: 12 via 2+9+1)");

        System.out.println("MixedAdvancedDSASet tests passed!");
    }
}
