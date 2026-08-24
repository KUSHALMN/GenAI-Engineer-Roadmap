import java.util.*;

/**
 * Problem: Course Schedule (LeetCode 207)
 * 
 * There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
 * You are given an array prerequisites where prerequisites[i] = [a_i, b_i] indicates that
 * you must take course b_i first if you want to take course a_i.
 * 
 * Return true if you can finish all courses, otherwise return false.
 * 
 * Fundamental Concepts:
 * - Cycle detection in a Directed Graph.
 * - If Directed Acyclic Graph (DAG) => True (Topological Sort exists).
 * - If cycle exists => False.
 * 
 * Approaches:
 * 1. Kahn's Algorithm (BFS In-Degree Topological Sort):
 *    - Time Complexity: O(V + E)
 *    - Space Complexity: O(V + E) for adjacency list, in-degree array, and queue.
 * 
 * 2. 3-State DFS Cycle Detection (Graph Coloring):
 *    - 0 = UNVISITED
 *    - 1 = VISITING (currently in recursion call stack => Back-edge detected if re-encountered!)
 *    - 2 = VISITED (fully explored branch)
 *    - Time Complexity: O(V + E)
 *    - Space Complexity: O(V + E) for graph adjacency list and recursion stack.
 */
public class course_schedule {

    // ==========================================
    // Approach 1: Kahn's Algorithm (BFS)
    // ==========================================
    public static boolean canFinishBFS(int numCourses, int[][] prerequisites) {
        if (numCourses <= 0) return true;
        if (prerequisites == null || prerequisites.length == 0) return true;

        List<List<Integer>> adj = new ArrayList<>(numCourses);
        int[] inDegree = new int[numCourses];

        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList<>());
        }

        // Build Graph: prereq (edge[1]) -> course (edge[0])
        for (int[] edge : prerequisites) {
            int course = edge[0];
            int prereq = edge[1];
            adj.get(prereq).add(course);
            inDegree[course]++;
        }

        // Enqueue nodes with 0 in-degree
        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) {
                queue.offer(i);
            }
        }

        int processedCourses = 0;

        while (!queue.isEmpty()) {
            int curr = queue.poll();
            processedCourses++;

            for (int neighbor : adj.get(curr)) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    queue.offer(neighbor);
                }
            }
        }

        return processedCourses == numCourses;
    }

    // ==========================================
    // Approach 2: DFS 3-State Cycle Detection
    // ==========================================
    private static final int UNVISITED = 0;
    private static final int VISITING = 1;
    private static final int VISITED = 2;

    public static boolean canFinishDFS(int numCourses, int[][] prerequisites) {
        if (numCourses <= 0) return true;
        if (prerequisites == null || prerequisites.length == 0) return true;

        List<List<Integer>> adj = new ArrayList<>(numCourses);
        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList<>());
        }

        for (int[] edge : prerequisites) {
            adj.get(edge[1]).add(edge[0]);
        }

        int[] state = new int[numCourses];

        for (int i = 0; i < numCourses; i++) {
            if (state[i] == UNVISITED) {
                if (hasCycleDFS(i, adj, state)) {
                    return false; // Cycle detected
                }
            }
        }

        return true;
    }

    private static boolean hasCycleDFS(int node, List<List<Integer>> adj, int[] state) {
        state[node] = VISITING;

        for (int neighbor : adj.get(node)) {
            if (state[neighbor] == VISITING) {
                return true; // Back-edge detected
            }
            if (state[neighbor] == UNVISITED) {
                if (hasCycleDFS(neighbor, adj, state)) {
                    return true;
                }
            }
        }

        state[node] = VISITED;
        return false;
    }

    // ==========================================
    // Test Suite and Main Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("    LeetCode 207: Course Schedule Test Suite     ");
        System.out.println("=================================================\n");

        // Test 1: Simple DAG (0 -> 1)
        int num1 = 2;
        int[][] pre1 = {{1, 0}};
        runTestCase("Test 1: Simple 2-Course DAG", num1, pre1, true);

        // Test 2: Simple Cycle (0 -> 1 and 1 -> 0)
        int num2 = 2;
        int[][] pre2 = {{1, 0}, {0, 1}};
        runTestCase("Test 2: Direct 2-Course Cycle", num2, pre2, false);

        // Test 3: Diamond DAG (0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3)
        int num3 = 4;
        int[][] pre3 = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        runTestCase("Test 3: Diamond DAG (4 Courses)", num3, pre3, true);

        // Test 4: Cycle in sub-graph (1 -> 2 -> 3 -> 1)
        int num4 = 4;
        int[][] pre4 = {{1, 0}, {2, 1}, {3, 2}, {1, 3}};
        runTestCase("Test 4: 3-Node Cycle in 4 Courses", num4, pre4, false);

        // Test 5: Disconnected Components
        int num5 = 5;
        int[][] pre5 = {{1, 0}, {3, 2}};
        runTestCase("Test 5: Disconnected Forest DAG", num5, pre5, true);

        // Test 6: Self loop (0 -> 0)
        int num6 = 1;
        int[][] pre6 = {{0, 0}};
        runTestCase("Test 6: Self Loop Cycle", num6, pre6, false);

        System.out.println("\nAll Course Schedule test cases passed successfully!");
    }

    private static void runTestCase(String label, int numCourses, int[][] prereqs, boolean expected) {
        boolean bfs = canFinishBFS(numCourses, prereqs);
        boolean dfs = canFinishDFS(numCourses, prereqs);

        boolean ok = (bfs == expected && dfs == expected);
        System.out.printf("[%s] Expected: %b | BFS: %b | DFS: %b => %s%n",
                label, expected, bfs, dfs, (ok ? "PASSED" : "FAILED"));

        if (!ok) {
            throw new AssertionError("Test case failed: " + label);
        }
    }
}
