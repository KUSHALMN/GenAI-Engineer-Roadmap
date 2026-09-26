import java.util.*;

/**
 * Backtracking Patterns in Java
 *
 * Problems Covered:
 *   1. LeetCode 78 - Subsets -> O(2^N) time, O(N) space
 *   2. LeetCode 46 - Permutations -> O(N! * N) time, O(N) space
 *   3. LeetCode 51 - N-Queens -> O(N!) time, O(N) space
 */
public class BacktrackingPatterns {

    /**
     * LC 78: Subsets
     */
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrackSubsets(0, nums, new ArrayList<>(), result);
        return result;
    }

    private void backtrackSubsets(int start, int[] nums, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current));
        for (int i = start; i < nums.length; i++) {
            current.add(nums[i]);
            backtrackSubsets(i + 1, nums, current, result);
            current.remove(current.size() - 1);
        }
    }

    /**
     * LC 46: Permutations
     */
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        boolean[] used = new boolean[nums.length];
        backtrackPermute(nums, used, new ArrayList<>(), result);
        return result;
    }

    private void backtrackPermute(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
        if (current.size() == nums.length) {
            result.add(new ArrayList<>(current));
            return;
        }

        for (int i = 0; i < nums.length; i++) {
            if (!used[i]) {
                used[i] = true;
                current.add(nums[i]);
                backtrackPermute(nums, used, current, result);
                current.remove(current.size() - 1);
                used[i] = false;
            }
        }
    }

    /**
     * LC 51: N-Queens
     */
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        char[][] board = new char[n][n];
        for (int i = 0; i < n; i++) Arrays.fill(board[i], '.');

        Set<Integer> cols = new HashSet<>();
        Set<Integer> diag1 = new HashSet<>(); // r - c
        Set<Integer> diag2 = new HashSet<>(); // r + c

        backtrackQueens(0, n, board, cols, diag1, diag2, result);
        return result;
    }

    private void backtrackQueens(int r, int n, char[][] board, Set<Integer> cols, Set<Integer> diag1, Set<Integer> diag2, List<List<String>> result) {
        if (r == n) {
            List<String> solution = new ArrayList<>();
            for (int i = 0; i < n; i++) solution.add(new String(board[i]));
            result.add(solution);
            return;
        }

        for (int c = 0; c < n; c++) {
            if (cols.contains(c) || diag1.contains(r - c) || diag2.contains(r + c)) {
                continue;
            }

            cols.add(c);
            diag1.add(r - c);
            diag2.add(r + c);
            board[r][c] = 'Q';

            backtrackQueens(r + 1, n, board, cols, diag1, diag2, result);

            cols.remove(c);
            diag1.remove(r - c);
            diag2.remove(r + c);
            board[r][c] = '.';
        }
    }

    public static void main(String[] args) {
        BacktrackingPatterns bp = new BacktrackingPatterns();

        // 1. Subsets
        List<List<Integer>> subs = bp.subsets(new int[]{1, 2, 3});
        System.out.println("LC 78 Subsets Count: " + subs.size()); // 8

        // 2. Permutations
        List<List<Integer>> perms = bp.permute(new int[]{1, 2, 3});
        System.out.println("LC 46 Permutations Count: " + perms.size()); // 6

        // 3. N-Queens
        List<List<String>> n4 = bp.solveNQueens(4);
        System.out.println("LC 51 N-Queens (N=4) Solutions Count: " + n4.size()); // 2
    }
}
