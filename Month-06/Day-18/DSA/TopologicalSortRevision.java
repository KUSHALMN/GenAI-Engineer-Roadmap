import java.util.*;

public class TopologicalSortRevision {
    // LC 207 & 210: Course Schedule II (Kahn's BFS)
    public static int[] findOrder(int numCourses, int[][] prerequisites) {
        int[] inDegree = new int[numCourses];
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        for (int[] p : prerequisites) {
            adj.get(p[1]).add(p[0]);
            inDegree[p[0]]++;
        }

        Queue<Integer> q = new ArrayDeque<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }

        int[] order = new int[numCourses];
        int idx = 0;
        while (!q.isEmpty()) {
            int u = q.poll();
            order[idx++] = u;
            for (int v : adj.get(u)) {
                inDegree[v]--;
                if (inDegree[v] == 0) q.offer(v);
            }
        }
        return idx == numCourses ? order : new int[0];
    }

    public static void main(String[] args) {
        System.out.println("=== Topological Sort Verification ===");
        int[][] pre = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        int[] order = findOrder(4, pre);
        System.out.println("LC 210 (Course Schedule II): " + Arrays.toString(order));
        assert order.length == 4 && order[0] == 0 : "LC 210 failed";
        System.out.println("Topological sort passed!");
    }
}
