import java.util.*;

/**
 * Day 23: Disjoint Set Union — Redundant Connection
 * Problem: A tree with n nodes has one additional edge added.
 * Return an edge that can be removed so that the resulting graph is a tree of n nodes.
 *
 * Algorithm:
 * - Initialize DSU for vertices 1 to n.
 * - For each edge (u, v):
 *   If find(u) == find(v), this edge creates a cycle (redundant edge).
 *   Else union(u, v).
 *
 * Time Complexity: O(N * alpha(N))
 * Space Complexity: O(N)
 */
public class RedundantConnection {

    static class DSU {
        int[] parent;
        DSU(int n) {
            parent = new int[n + 1];
            for (int i = 0; i <= n; i++) parent[i] = i;
        }
        int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }
        boolean union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);
            if (rootX == rootY) return false; // Cycle detected
            parent[rootX] = rootY;
            return true;
        }
    }

    public int[] findRedundantConnection(int[][] edges) {
        DSU dsu = new DSU(edges.length);
        for (int[] edge : edges) {
            if (!dsu.union(edge[0], edge[1])) {
                return edge;
            }
        }
        return new int[0];
    }

    public static void main(String[] args) {
        RedundantConnection solver = new RedundantConnection();
        int[][] edges = {{1, 2}, {1, 3}, {2, 3}};
        int[] redundant = solver.findRedundantConnection(edges);

        System.out.println("Redundant edge: [" + redundant[0] + ", " + redundant[1] + "]");
        assert redundant[0] == 2 && redundant[1] == 3 : "Expected [2, 3]";
        System.out.println("Day 23 DSA RedundantConnection verification passed!");
    }
}
