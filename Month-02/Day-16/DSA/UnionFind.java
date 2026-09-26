import java.util.Arrays;

/**
 * Disjoint Set Union (Union-Find) with Path Compression and Union by Rank in Java
 *
 * Problems Covered:
 *   1. LeetCode 547 - Number of Provinces -> O(N^2 * alpha(N)) time, O(N) space
 *   2. LeetCode 684 - Redundant Connection -> O(N * alpha(N)) time, O(N) space
 */
public class UnionFind {

    private final int[] parent;
    private final int[] rank;
    private int count;

    public UnionFind(int size) {
        parent = new int[size];
        rank = new int[size];
        count = size;
        for (int i = 0; i < size; i++) {
            parent[i] = i;
            rank[i] = 1;
        }
    }

    public int find(int p) {
        if (parent[p] != p) {
            parent[p] = find(parent[p]); // Path compression
        }
        return parent[p];
    }

    public boolean union(int p, int q) {
        int rootP = find(p);
        int rootQ = find(q);

        if (rootP == rootQ) return false;

        // Union by rank
        if (rank[rootP] > rank[rootQ]) {
            parent[rootQ] = rootP;
        } else if (rank[rootP] < rank[rootQ]) {
            parent[rootP] = rootQ;
        } else {
            parent[rootQ] = rootP;
            rank[rootP]++;
        }

        count--;
        return true;
    }

    public int getCount() {
        return count;
    }

    // LeetCode 547: Number of Provinces
    public static int findCircleNum(int[][] isConnected) {
        int n = isConnected.length;
        UnionFind uf = new UnionFind(n);

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (isConnected[i][j] == 1) {
                    uf.union(i, j);
                }
            }
        }
        return uf.getCount();
    }

    // LeetCode 684: Redundant Connection
    public static int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        UnionFind uf = new UnionFind(n + 1);

        for (int[] edge : edges) {
            int u = edge[0];
            int v = edge[1];
            if (!uf.union(u, v)) {
                return edge;
            }
        }
        return new int[0];
    }

    public static void main(String[] args) {
        // 1. Number of Provinces
        int[][] connected = {
            {1, 1, 0},
            {1, 1, 0},
            {0, 0, 1}
        };
        int provinces = findCircleNum(connected);
        System.out.println("LC 547 Number of Provinces: " + provinces); // 2

        // 2. Redundant Connection
        int[][] edges = {{1, 2}, {1, 3}, {2, 3}};
        int[] redundant = findRedundantConnection(edges);
        System.out.println("LC 684 Redundant Edge: " + Arrays.toString(redundant)); // [2, 3]
    }
}
