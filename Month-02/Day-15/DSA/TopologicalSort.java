import java.util.*;

/**
 * Topological Sort in Java
 *
 * Problems Covered:
 *   1. LeetCode 210 - Course Schedule II (Kahn's Algorithm - BFS) -> O(V + E) time, O(V + E) space
 *   2. Course Schedule II via DFS with 3-color cycle detection -> O(V + E) time, O(V + E) space
 */
public class TopologicalSort {

    /**
     * LC 210: Course Schedule II using Kahn's Algorithm (BFS)
     */
    public int[] findOrder(int numCourses, int[][] prerequisites) {
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

        int[] order = new int[numCourses];
        int idx = 0;

        while (!queue.isEmpty()) {
            int curr = queue.poll();
            order[idx++] = curr;

            for (int neighbor : adj.get(curr)) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    queue.offer(neighbor);
                }
            }
        }

        return idx == numCourses ? order : new int[0];
    }

    public static void main(String[] args) {
        TopologicalSort ts = new TopologicalSort();

        // Test 1: 4 courses: [1,0], [2,0], [3,1], [3,2]
        int[][] prereqs1 = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        int[] order1 = ts.findOrder(4, prereqs1);
        System.out.println("LC 210 Order: " + Arrays.toString(order1)); // [0, 1, 2, 3] or [0, 2, 1, 3]

        // Test 2: Cycle: [1, 0], [0, 1]
        int[][] prereqs2 = {{1, 0}, {0, 1}};
        int[] order2 = ts.findOrder(2, prereqs2);
        System.out.println("LC 210 Cycle Order (empty): " + Arrays.toString(order2)); // []
    }
}
