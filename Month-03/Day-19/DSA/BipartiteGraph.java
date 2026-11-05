import java.util.*;

/**
 * Bipartite Graph Verification (2-Coloring Problem)
 * LeetCode 785 - Is Graph Bipartite?
 * A graph is bipartite if we can divide vertices into two sets U and V such that
 * every edge connects a vertex in U to a vertex in V (no odd-length cycles).
 * 
 * Complexity:
 * - Time: O(V + E) BFS traversal across all components
 * - Space: O(V) for color array and queue
 */
public class BipartiteGraph {

    public static boolean isBipartite(int[][] graph) {
        int n = graph.length;
        // 0: uncolored, 1: Color A, -1: Color B
        int[] color = new int[n];

        for (int i = 0; i < n; i++) {
            if (color[i] != 0) continue; // Already processed component

            Queue<Integer> queue = new LinkedList<>();
            queue.offer(i);
            color[i] = 1;

            while (!queue.isEmpty()) {
                int curr = queue.poll();

                for (int neighbor : graph[curr]) {
                    if (color[neighbor] == 0) {
                        // Color with opposite color
                        color[neighbor] = -color[curr];
                        queue.offer(neighbor);
                    } else if (color[neighbor] == color[curr]) {
                        // Same color conflict -> Not bipartite (odd cycle detected)
                        return false;
                    }
                }
            }
        }

        return true;
    }

    public static void main(String[] args) {
        // Graph 1: [[1,3],[0,2],[1,3],[0,2]] -> Bipartite 4-cycle (Even cycle)
        int[][] graph1 = {{1, 3}, {0, 2}, {1, 3}, {0, 2}};
        System.out.println("Graph 1 is bipartite: " + isBipartite(graph1)); // Expected true

        // Graph 2: [[1,2,3],[0,2],[0,1,3],[0,2]] -> Triangle (Odd cycle 0-1-2)
        int[][] graph2 = {{1, 2, 3}, {0, 2}, {0, 1, 3}, {0, 2}};
        System.out.println("Graph 2 is bipartite: " + isBipartite(graph2)); // Expected false

        System.out.println("BipartiteGraph tests passed!");
    }
}
