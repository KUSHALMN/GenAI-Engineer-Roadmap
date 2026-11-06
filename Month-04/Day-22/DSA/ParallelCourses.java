import java.util.*;

/**
 * Day 22: Topological Sort — Parallel Courses
 * Problem: Given n courses labeled 1 to n and relations[i] = [prevCourse, nextCourse],
 * find the minimum number of semesters needed to take all courses. If impossible, return -1.
 *
 * Algorithm:
 * - Kahn's algorithm (BFS topological sort) level by level.
 * - Each BFS level represents one semester of parallel courses.
 *
 * Time Complexity: O(V + E)
 * Space Complexity: O(V + E)
 */
public class ParallelCourses {

    public int minimumSemesters(int n, int[][] relations) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
        int[] inDegree = new int[n + 1];

        for (int[] r : relations) {
            adj.get(r[0]).add(r[1]);
            inDegree[r[1]]++;
        }

        Queue<Integer> q = new LinkedList<>();
        for (int i = 1; i <= n; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }

        int semesters = 0;
        int takenCourses = 0;

        while (!q.isEmpty()) {
            int size = q.size();
            semesters++;
            takenCourses += size;

            for (int i = 0; i < size; i++) {
                int curr = q.poll();
                for (int next : adj.get(curr)) {
                    if (--inDegree[next] == 0) {
                        q.offer(next);
                    }
                }
            }
        }
        return takenCourses == n ? semesters : -1;
    }

    public static void main(String[] args) {
        ParallelCourses solver = new ParallelCourses();
        int n = 3;
        int[][] relations = {{1, 3}, {2, 3}};
        int sem = solver.minimumSemesters(n, relations);

        System.out.println("Minimum semesters for courses: " + sem);
        assert sem == 2 : "Expected 2 semesters (courses 1 & 2 in sem 1, course 3 in sem 2)";
        System.out.println("Day 22 DSA ParallelCourses verification passed!");
    }
}
