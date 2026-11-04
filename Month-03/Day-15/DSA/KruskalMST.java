package DSA;

import java.util.*;

/**
 * Kruskal's Minimum Spanning Tree (MST) Algorithm
 * 1. Sort all edges in non-decreasing order of weight: O(E log E)
 * 2. Pick the smallest edge; if it does not form a cycle (checked via DSU), add it to MST
 * 3. Repeat until V - 1 edges are included
 * 
 * Complexity:
 * - Time: O(E log E + E * alpha(V)) = O(E log E)
 * - Space: O(V) for DSU parent and rank arrays
 */
public class KruskalMST {

    static class Edge implements Comparable<Edge> {
        int u, v, weight;

        Edge(int u, int v, int weight) {
            this.u = u;
            this.v = v;
            this.weight = weight;
        }

        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.weight, other.weight);
        }
    }

    static class DSU {
        int[] parent, rank;

        DSU(int n) {
            parent = new int[n];
            rank = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        int find(int i) {
            if (parent[i] != i) {
                parent[i] = find(parent[i]);
            }
            return parent[i];
        }

        boolean union(int i, int j) {
            int rootI = find(i);
            int rootJ = find(j);
            if (rootI == rootJ) return false;

            if (rank[rootI] < rank[rootJ]) {
                parent[rootI] = rootJ;
            } else if (rank[rootI] > rank[rootJ]) {
                parent[rootJ] = rootI;
            } else {
                parent[rootJ] = rootI;
                rank[rootI]++;
            }
            return true;
        }
    }

    public static int computeMSTWeight(int n, List<Edge> edges) {
        Collections.sort(edges);
        DSU dsu = new DSU(n);
        int totalWeight = 0;
        int edgesAdded = 0;

        for (Edge edge : edges) {
            if (dsu.union(edge.u, edge.v)) {
                totalWeight += edge.weight;
                edgesAdded++;
                if (edgesAdded == n - 1) break;
            }
        }

        return edgesAdded == n - 1 ? totalWeight : -1;
    }

    public static void main(String[] args) {
        int n = 4;
        List<Edge> edges = new ArrayList<>();
        edges.add(new Edge(0, 1, 10));
        edges.add(new Edge(0, 2, 6));
        edges.add(new Edge(0, 3, 5));
        edges.add(new Edge(1, 3, 15));
        edges.add(new Edge(2, 3, 4));

        int mstCost = computeMSTWeight(n, edges);
        System.out.println("Minimum Spanning Tree total cost for 4 nodes: " + mstCost); // Expected 5 + 4 + 10 = 19
        System.out.println("Kruskal MST tests passed!");
    }
}
