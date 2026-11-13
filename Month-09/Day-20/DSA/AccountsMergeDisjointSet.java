package Month_09.Day_20.DSA;

import java.util.*;

/**
 * Day 20: Timed DSA Problem Set — Disjoint Set Union (DSU) Graph Clustering.
 * Focus: LeetCode 721 (Accounts Merge) - O(N * K * log(N * K)) Time, O(N * K) Space.
 */
public class AccountsMergeDisjointSet {

    private static class DSU {
        private final int[] parent;

        public DSU(int n) {
            parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        public int find(int i) {
            if (parent[i] == i) return i;
            return parent[i] = find(parent[i]); // Path compression
        }

        public void union(int i, int j) {
            int rootI = find(i);
            int rootJ = find(j);
            if (rootI != rootJ) {
                parent[rootI] = rootJ;
            }
        }
    }

    public static List<List<String>> accountsMerge(List<List<String>> accounts) {
        int n = accounts.size();
        DSU dsu = new DSU(n);
        Map<String, Integer> emailToAccount = new HashMap<>();

        // 1. Map emails to account index and union accounts sharing emails
        for (int i = 0; i < n; i++) {
            List<String> acc = accounts.get(i);
            for (int j = 1; j < acc.size(); j++) {
                String email = acc.get(j);
                if (emailToAccount.containsKey(email)) {
                    dsu.union(i, emailToAccount.get(email));
                } else {
                    emailToAccount.put(email, i);
                }
            }
        }

        // 2. Group emails by their canonical parent account index
        Map<Integer, TreeSet<String>> merged = new HashMap<>();
        for (int i = 0; i < n; i++) {
            int root = dsu.find(i);
            merged.computeIfAbsent(root, k -> new TreeSet<>());
            List<String> acc = accounts.get(i);
            for (int j = 1; j < acc.size(); j++) {
                merged.get(root).add(acc.get(j));
            }
        }

        // 3. Construct final output format
        List<List<String>> result = new ArrayList<>();
        for (Map.Entry<Integer, TreeSet<String>> entry : merged.entrySet()) {
            List<String> res = new ArrayList<>();
            res.add(accounts.get(entry.getKey()).get(0)); // User Name
            res.addAll(entry.getValue()); // Sorted unique emails
            result.add(res);
        }
        return result;
    }

    public static void main(String[] args) {
        List<List<String>> accounts = List.of(
            List.of("John", "johnsmith@mail.com", "john_newyork@mail.com"),
            List.of("John", "johnsmith@mail.com", "john00@mail.com"),
            List.of("Mary", "mary@mail.com"),
            List.of("John", "johnnybravo@mail.com")
        );

        List<List<String>> merged = accountsMerge(accounts);
        assert merged.size() == 3 : "Merged count should be 3";

        System.out.println("Day 20 Accounts Merge DSU verification passed.");
    }
}
