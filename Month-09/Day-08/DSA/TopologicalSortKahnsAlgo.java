package Month_09.Day_08.DSA;

import java.util.*;

/**
 * Day 08: Timed DSA Problem Set — Topological Sort using Kahn's In-Degree Algorithm.
 * Focus: LeetCode 210 (Course Schedule II) - O(V + E) Time, O(V + E) Space.
 */
public class TopologicalSortKahnsAlgo {

    public static int[] findOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>(numCourses);
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        int[] inDegree = new int[numCourses];

        for (int[] pre : prerequisites) {
            int course = pre[0];
            int prerequisite = pre[1];
            adj.get(prerequisite).add(course);
            inDegree[course]++;
        }

        Queue<Integer> queue = new ArrayDeque<>();
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

        // If index == numCourses, a valid topological order exists; otherwise there is a cycle
        return index == numCourses ? order : new int[0];
    }

    public static void main(String[] args) {
        int[][] pre1 = {{1, 0}};
        int[] res1 = findOrder(2, pre1);
        assert Arrays.equals(res1, new int[]{0, 1}) : "Test 1 Failed";

        int[][] pre2 = {{1,0},{2,0},{3,1},{3,2}};
        int[] res2 = findOrder(4, pre2);
        assert res2.length == 4 && res2[0] == 0 : "Test 2 Failed";

        int[][] cycle = {{1, 0}, {0, 1}};
        int[] resCycle = findOrder(2, cycle);
        assert resCycle.length == 0 : "Cycle detection failed";

        System.out.println("Day 08 Topological Sort Kahn's Algo verification passed.");
    }
}
