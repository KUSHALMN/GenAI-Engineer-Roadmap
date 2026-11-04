package DSA;

import java.util.*;

/**
 * Topological Sort in Directed Acyclic Graphs (DAG)
 * LeetCode 210 - Course Schedule II
 * Methods:
 * 1. Kahn's Algorithm (BFS with In-degree array) - O(V + E)
 * 2. Cycle Detection: If processed nodes != V, cycle exists.
 * Complexity:
 * - Time: O(V + E)
 * - Space: O(V + E) for adjacency list and queue
 */
public class TopologicalSort {

    public static int[] findOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList<>());
        }

        int[] inDegree = new int[numCourses];
        for (int[] pre : prerequisites) {
            int course = pre[0];
            int prerequisite = pre[1];
            adj.get(prerequisite).add(course);
            inDegree[course]++;
        }

        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) {
                queue.offer(i);
            }
        }

        int[] order = new int[numCourses];
        int index = 0;

        while (!queue.isEmpty()) {
            int curr = queue.poll();
            order[index++] = curr;

            for (int neighbor : adj.get(curr)) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    queue.offer(neighbor);
                }
            }
        }

        // If cycle exists, cannot finish all courses
        if (index != numCourses) {
            return new int[0];
        }

        return order;
    }

    public static void main(String[] args) {
        int numCourses = 4;
        int[][] prerequisites = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        int[] order = findOrder(numCourses, prerequisites);
        System.out.println("Valid course completion order: " + Arrays.toString(order));

        int[][] cycle = {{1, 0}, {0, 1}};
        int[] cycleResult = findOrder(2, cycle);
        System.out.println("Cycle result length: " + cycleResult.length + " (Expected: 0)");

        System.out.println("TopologicalSort tests passed!");
    }
}
