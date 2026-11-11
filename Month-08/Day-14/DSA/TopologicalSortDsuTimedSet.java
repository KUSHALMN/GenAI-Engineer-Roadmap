package Month08.Day14;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

/**
 * Timed Set: Topological Sort & DSU
 * LC 210: Course Schedule II - O(V + E) Kahn's BFS with in-degree tracking.
 */
public class TopologicalSortDsuTimedSet {

    public static int[] findOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        int[] inDegree = new int[numCourses];

        for (int[] edge : prerequisites) {
            adj.get(edge[1]).add(edge[0]);
            inDegree[edge[0]]++;
        }

        Queue<Integer> queue = new ArrayDeque<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) queue.offer(i);
        }

        int[] order = new int[numCourses];
        int idx = 0;

        while (!queue.isEmpty()) {
            int course = queue.poll();
            order[idx++] = course;
            for (int neighbor : adj.get(course)) {
                if (--inDegree[neighbor] == 0) {
                    queue.offer(neighbor);
                }
            }
        }
        return idx == numCourses ? order : new int[0];
    }

    public static void main(String[] args) {
        int[][] pre = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        int[] order = findOrder(4, pre);
        assert order.length == 4;
        assert order[0] == 0;

        System.out.println("Day 14 Topological Sort & DSU Timed Set verification passed.");
    }
}
