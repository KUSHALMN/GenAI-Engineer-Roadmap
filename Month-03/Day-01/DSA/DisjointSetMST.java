package DSA;

import java.util.*;

/**
 * Day 01 (Month 03) DSA: Disjoint Set Union (DSU) & Minimum Spanning Tree (MST)
 * - DSU with Path Compression and Union by Rank
 * - LeetCode 547: Number of Provinces (Connected Components)
 * - LeetCode 684: Redundant Connection (Cycle Detection)
 * - LeetCode 1584: Min Cost to Connect All Points (Kruskal's Algorithm)
 */
public class DisjointSetMST {

    public static class DSU {
        private final int[] parent;
        private final int[] rank;
        private int count;

        public DSU(int n) {
            parent = new int[n];
            rank = new int[n];
            count = n;
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                rank[i] = 0;
            }
        }

        public int find(int i) {
            if (parent[i] == i) return i;
            return parent[i] = find(parent[i]); // Path compression
        }

        public boolean union(int i, int j) {
            int rootI = find(i);
            int rootJ = find(j);
            if (rootI == rootJ) return false; // Already connected

            // Union by rank
            if (rank[rootI] < rank[rootJ]) {
                parent[rootI] = rootJ;
            } else if (rank[rootI] > rank[rootJ]) {
                parent[rootJ] = rootI;
            } else {
                parent[rootJ] = rootI;
                rank[rootI]++;
            }
            count--;
            return true;
        }

        public int getCount() {
            return count;
        }
    }

    // -------------------------------------------------------------
    // LC 547: Number of Provinces
    // -------------------------------------------------------------
    public static int findCircleNum(int[][] isConnected) {
        int n = isConnected.length;
        DSU dsu = new DSU(n);
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (isConnected[i][j] == 1) {
                    dsu.union(i, j);
                }
            }
        }
        return dsu.getCount();
    }

    // -------------------------------------------------------------
    // LC 684: Redundant Connection
    // -------------------------------------------------------------
    public static int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        DSU dsu = new DSU(n + 1); // 1-indexed nodes
        for (int[] edge : edges) {
            if (!dsu.union(edge[0], edge[1])) {
                return edge; // Found the redundant edge creating cycle
            }
        }
        return new int[0];
    }

    // -------------------------------------------------------------
    // LC 1584: Min Cost to Connect All Points (Kruskal's Algorithm)
    // -------------------------------------------------------------
    public static int minCostConnectPoints(int[][] points) {
        int n = points.length;
        List<int[]> edges = new ArrayList<>();

        // Generate all pairs and Manhattan distances
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int dist = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]);
                edges.add(new int[]{dist, i, j});
            }
        }

        // Sort edges by weight in ascending order
        edges.sort(Comparator.comparingInt(a -> a[0]));

        DSU dsu = new DSU(n);
        int totalCost = 0;
        int edgesAdded = 0;

        for (int[] edge : edges) {
            int weight = edge[0];
            int u = edge[1];
            int v = edge[2];
            if (dsu.union(u, v)) {
                totalCost += weight;
                edgesAdded++;
                if (edgesAdded == n - 1) break;
            }
        }
        return totalCost;
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Month 03 Day 01: DSU & Kruskal's MST Suite");
        System.out.println("==================================================");

        // Test 1: LC 547 Provinces
        int[][] isConnected = {
            {1, 1, 0},
            {1, 1, 0},
            {0, 0, 1}
        };
        int provinces = findCircleNum(isConnected);
        System.out.println("LC 547 (Provinces): " + provinces);
        assert provinces == 2 : "LC 547 Failed";

        // Test 2: LC 684 Redundant Connection
        int[][] edges = {{1, 2}, {1, 3}, {2, 3}};
        int[] redEdge = findRedundantConnection(edges);
        System.out.println("LC 684 (Redundant Edge): " + Arrays.toString(redEdge));
        assert Arrays.equals(redEdge, new int[]{2, 3}) : "LC 684 Failed";

        // Test 3: LC 1584 Min Cost to Connect All Points
        int[][] points = {{0, 0}, {2, 2}, {3, 10}, {5, 2}, {7, 0}};
        int minCost = minCostConnectPoints(points);
        System.out.println("LC 1584 (Min Cost to Connect Points): " + minCost);
        assert minCost == 20 : "LC 1584 Failed";

        System.out.println("\nAll Java DSU & MST tests executed successfully! [OK]");
    }
}
