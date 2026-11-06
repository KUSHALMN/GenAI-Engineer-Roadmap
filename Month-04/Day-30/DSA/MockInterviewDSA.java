import java.util.*;

/**
 * Day 30: DSA Mock Interview — Topological Sort & Backtracking
 * Problem 1: Course Schedule II (Find ordering of courses).
 * Problem 2: Target Sum (Ways to assign + / - to reach target).
 *
 * Time Complexity: Course Schedule II: O(V + E) | Target Sum: O(N * Target)
 * Space Complexity: Course Schedule II: O(V + E) | Target Sum: O(N * Target)
 */
public class MockInterviewDSA {

    // Problem 1: Course Schedule II
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        int[] inDegree = new int[numCourses];

        for (int[] p : prerequisites) {
            adj.get(p[1]).add(p[0]);
            inDegree[p[0]]++;
        }

        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) q.offer(i);
        }

        int[] order = new int[numCourses];
        int idx = 0;

        while (!q.isEmpty()) {
            int curr = q.poll();
            order[idx++] = curr;
            for (int next : adj.get(curr)) {
                if (--inDegree[next] == 0) q.offer(next);
            }
        }
        return idx == numCourses ? order : new int[0];
    }

    // Problem 2: Target Sum using DP (Subset Sum transformation)
    public int findTargetSumWays(int[] nums, int target) {
        int total = 0;
        for (int x : nums) total += x;
        if (Math.abs(target) > total || (total + target) % 2 != 0) return 0;

        int s1 = (total + target) / 2;
        int[] dp = new int[s1 + 1];
        dp[0] = 1;

        for (int num : nums) {
            for (int j = s1; j >= num; j--) {
                dp[j] += dp[j - num];
            }
        }
        return dp[s1];
    }

    public static void main(String[] args) {
        MockInterviewDSA mock = new MockInterviewDSA();

        // Test Problem 1
        int[][] prereqs = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        int[] order = mock.findOrder(4, prereqs);
        System.out.println("Course Schedule II order: " + Arrays.toString(order));
        assert order.length == 4;

        // Test Problem 2
        int[] nums = {1, 1, 1, 1, 1};
        int ways = mock.findTargetSumWays(nums, 3);
        System.out.println("Target Sum ways for target 3: " + ways);
        assert ways == 5 : "Expected 5 ways";

        System.out.println("Day 30 DSA Mock Interview passed successfully!");
    }
}
