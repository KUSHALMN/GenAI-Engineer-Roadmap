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
 * Fundamental Concept:
 * - Detect if the directed graph contains a cycle.
 * - If DAG (Directed Acyclic Graph) => true (Topological Sort exists).
 * - If contains cycle => false.
 * 
 * Approaches:
 * 1. Kahn's Algorithm (BFS Topological Sort / In-Degree Array):
 *    - Compute in-degree for every vertex.
 *    - Enqueue all vertices with in-degree == 0.
 *    - Process queue: for each course, reduce in-degree of its neighbors.
 *    - If neighbor's in-degree reaches 0, enqueue it.
 *    - If processed count == numCourses, no cycle exists.
 *    - Time Complexity: O(V + E)
 *    - Space Complexity: O(V + E) for adjacency list + in-degree array + queue.
 * 
 * 2. Depth-First Search (DFS 3-State Cycle Detection):
 *    - 0 = UNVISITED
 *    - 1 = VISITING (currently in recursion call stack => Back-edge detected if re-encountered!)
 *    - 2 = VISITED (fully explored branch)
 *    - Time Complexity: O(V + E)
 *    - Space Complexity: O(V + E) for graph + recursion stack.
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

        // Build Graph: prerequisite[1] -> prerequisite[0]
        for (int[] edge : prerequisites) {
            int course = edge[0];
            int prereq = edge[1];
            adj.get(prereq).add(course);
            inDegree[course]++;
        }

        // Push all nodes with 0 in-degree into Queue
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
    // Approach 2: DFS Cycle Detection (3 States)
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
                return true; // Found back-edge to an active ancestor in recursion stack!
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
    // Verification & Test Suite
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("    LeetCode 207: Course Schedule Test Suite     ");
        System.out.println("=================================================\n");

        // Test Case 1: Simple DAG [1, 0] -> 0 before 1 (Valid)
        int num1 = 2;
        int[][] pre1 = {{1, 0}};
        runTest("Test Case 1 (Simple 2-Course DAG)", num1, pre1, true);

        // Test Case 2: Simple Cycle [1, 0], [0, 1] (Invalid)
        int num2 = 2;
        int[][] pre2 = {{1, 0}, {0, 1}};
        runTest("Test Case 2 (Direct 2-Course Cycle)", num2, pre2, false);

        // Test Case 3: 4 Courses DAG
        // 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
        int num3 = 4;
        int[][] pre3 = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        runTest("Test Case 3 (Diamond DAG)", num3, pre3, true);

        // Test Case 4: 4 Courses with 3-node cycle (1 -> 2 -> 3 -> 1)
        int num4 = 4;
        int[][] pre4 = {{1, 0}, {2, 1}, {3, 2}, {1, 3}};
        runTest("Test Case 4 (3-Course Cycle in 4 Courses)", num4, pre4, false);

        // Test Case 5: Disconnected Courses without prerequisites
        int num5 = 5;
        int[][] pre5 = {{1, 0}, {3, 2}};
        runTest("Test Case 5 (Disconnected Forest DAG)", num5, pre5, true);

        // Test Case 6: Self loop [0, 0]
        int num6 = 1;
        int[][] pre6 = {{0, 0}};
        runTest("Test Case 6 (Self Loop)", num6, pre6, false);

        System.out.println("\nAll Course Schedule test cases passed successfully!");
    }

    private static void runTest(String label, int numCourses, int[][] prereqs, boolean expected) {
        boolean resBFS = canFinishBFS(numCourses, prereqs);
        boolean resDFS = canFinishDFS(numCourses, prereqs);

        boolean passed = (resBFS == expected) && (resDFS == expected);
        System.out.printf("[%s] => Expected: %b | BFS: %b | DFS: %b => %s%n",
                label, expected, resBFS, resDFS, (passed ? "PASSED" : "FAILED"));

        if (!passed) {
            throw new AssertionError("Test case failed: " + label);
        }
    }
}
