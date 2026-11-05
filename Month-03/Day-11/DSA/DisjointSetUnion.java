/**
 * Disjoint Set Union (DSU) / Union-Find with:
 * - Path Compression in find() -> amortized almost O(1) [Inverse Ackermann alpha(N)]
 * - Union by Rank/Size
 * Solves:
 * - LeetCode 323: Number of Connected Components in an Undirected Graph
 * - LeetCode 547: Number of Provinces
 */
public class DisjointSetUnion {
    private final int[] parent;
    private final int[] rank;
    private int count;

    public DisjointSetUnion(int n) {
        this.parent = new int[n];
        this.rank = new int[n];
        this.count = n;
        for (int i = 0; i < n; i++) {
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

        if (rootP == rootQ) {
            return false; // Already connected
        }

        // Union by rank
        if (rank[rootP] < rank[rootQ]) {
            parent[rootP] = rootQ;
        } else if (rank[rootP] > rank[rootQ]) {
            parent[rootQ] = rootP;
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

    /**
     * LC 323: Number of Connected Components in an Undirected Graph
     */
    public static int countComponents(int n, int[][] edges) {
        DisjointSetUnion dsu = new DisjointSetUnion(n);
        for (int[] edge : edges) {
            dsu.union(edge[0], edge[1]);
        }
        return dsu.getCount();
    }

    public static void main(String[] args) {
        int n = 5;
        int[][] edges = {{0, 1}, {1, 2}, {3, 4}};
        int components = countComponents(n, edges);
        System.out.println("Connected components for n=5, edges=[[0,1],[1,2],[3,4]]: " + components); // Expected 2

        int[][] singleGraph = {{0, 1}, {1, 2}, {2, 3}, {3, 4}};
        System.out.println("Connected components for fully connected graph: " + countComponents(5, singleGraph)); // Expected 1

        System.out.println("DisjointSetUnion tests passed!");
    }
}
