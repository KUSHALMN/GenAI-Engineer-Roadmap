package Month_09.Day_05.DSA;

import java.util.*;

/**
 * Day 05: Timed DSA Problem Set — Kruskal's Minimum Spanning Tree with DSU.
 * Focus: LeetCode 1135 (Connecting Cities With Minimum Cost) - O(E log E) Time, O(V) Space.
 */
public class KruskalsDisjointSetMst {

    public static class DisjointSetUnion {
        private final int[] parent;
        private final int[] rank;
        public int components;

        public DisjointSetUnion(int n) {
            this.parent = new int[n + 1];
            this.rank = new int[n + 1];
            this.components = n;
            for (int i = 1; i <= n; i++) parent[i] = i;
        }

        public int find(int i) {
            if (parent[i] == i) return i;
            return parent[i] = find(parent[i]); // Path compression
        }

        public boolean union(int i, int j) {
            int rootI = find(i);
            int rootJ = find(j);
            if (rootI == rootJ) return false;

            // Union by rank
            if (rank[rootI] < rank[rootJ]) {
                parent[rootI] = rootJ;
            } else if (rank[rootI] > rank[rootJ]) {
                parent[rootJ] = rootI;
            } else {
                parent[rootJ] = rootI;
                rank[rootI]++;
            }
            components--;
            return true;
        }
    }

    public static int minimumCost(int n, int[][] connections) {
        // Sort edges by weight in ascending order
        Arrays.sort(connections, Comparator.comparingInt(a -> a[2]));
        DisjointSetUnion dsu = new DisjointSetUnion(n);

        int totalCost = 0;
        int edgesUsed = 0;

        for (int[] edge : connections) {
            int u = edge[0], v = edge[1], cost = edge[2];
            if (dsu.union(u, v)) {
                totalCost += cost;
                edgesUsed++;
                if (edgesUsed == n - 1) {
                    return totalCost;
                }
            }
        }
        return -1; // Graph is disconnected
    }

    public static void main(String[] args) {
        int[][] conns1 = {{1,2,5},{1,3,6},{2,3,1}};
        assert minimumCost(3, conns1) == 6 : "Test 1 Failed";

        int[][] conns2 = {{1,2,3},{3,4,4}};
        assert minimumCost(4, conns2) == -1 : "Test 2 Failed";

        System.out.println("Day 05 Kruskal's MST & DSU verification passed.");
    }
}
