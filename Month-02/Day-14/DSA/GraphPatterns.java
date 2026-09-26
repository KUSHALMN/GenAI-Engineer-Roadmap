import java.util.*;

/**
 * Graph BFS, DFS & Cycle Detection in Java
 *
 * Problems Covered:
 *   1. LeetCode 200 - Number of Islands (DFS) -> O(M * N) time, O(M * N) space
 *   2. LeetCode 207 - Course Schedule (Cycle Detection via Kahn's BFS) -> O(V + E) time, O(V + E) space
 *   3. LeetCode 133 - Clone Graph (DFS with HashMap) -> O(V + E) time, O(V) space
 */
public class GraphPatterns {

    public static class Node {
        public int val;
        public List<Node> neighbors;
        public Node() { val = 0; neighbors = new ArrayList<>(); }
        public Node(int _val) { val = _val; neighbors = new ArrayList<>(); }
        public Node(int _val, ArrayList<Node> _neighbors) { val = _val; neighbors = _neighbors; }
    }

    /**
     * LC 200: Number of Islands
     */
    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        int rows = grid.length;
        int cols = grid[0].length;
        int count = 0;

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1') {
                    count++;
                    dfsIsland(grid, r, c, rows, cols);
                }
            }
        }
        return count;
    }

    private void dfsIsland(char[][] grid, int r, int c, int rows, int cols) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1') return;
        grid[r][c] = '0'; // visited
        dfsIsland(grid, r + 1, c, rows, cols);
        dfsIsland(grid, r - 1, c, rows, cols);
        dfsIsland(grid, r, c + 1, rows, cols);
        dfsIsland(grid, r, c - 1, rows, cols);
    }

    /**
     * LC 207: Course Schedule (Kahn's Topological Sort BFS)
     */
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        int[] inDegree = new int[numCourses];

        for (int[] p : prerequisites) {
            int dest = p[0];
            int src = p[1];
            adj.get(src).add(dest);
            inDegree[dest]++;
        }

        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) queue.offer(i);
        }

        int count = 0;
        while (!queue.isEmpty()) {
            int node = queue.poll();
            count++;
            for (int neighbor : adj.get(node)) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    queue.offer(neighbor);
                }
            }
        }

        return count == numCourses;
    }

    /**
     * LC 133: Clone Graph
     */
    public Node cloneGraph(Node node) {
        if (node == null) return null;
        Map<Node, Node> map = new HashMap<>();
        return dfsClone(node, map);
    }

    private Node dfsClone(Node node, Map<Node, Node> map) {
        if (map.containsKey(node)) return map.get(node);

        Node copy = new Node(node.val);
        map.put(node, copy);

        for (Node neighbor : node.neighbors) {
            copy.neighbors.add(dfsClone(neighbor, map));
        }
        return copy;
    }

    public static void main(String[] args) {
        GraphPatterns gp = new GraphPatterns();

        // 1. Number of Islands
        char[][] grid = {
            {'1', '1', '0', '0', '0'},
            {'1', '1', '0', '0', '0'},
            {'0', '0', '1', '0', '0'},
            {'0', '0', '0', '1', '1'}
        };
        int islands = gp.numIslands(grid);
        System.out.println("LC 200 Number of Islands: " + islands); // 3

        // 2. Course Schedule (No cycle)
        boolean can1 = gp.canFinish(2, new int[][]{{1, 0}});
        System.out.println("LC 207 Can Finish (No cycle): " + can1); // true

        // Course Schedule (Cycle)
        boolean can2 = gp.canFinish(2, new int[][]{{1, 0}, {0, 1}});
        System.out.println("LC 207 Can Finish (Cycle): " + can2); // false
    }
}
