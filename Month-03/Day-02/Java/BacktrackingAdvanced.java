import java.util.*;

/**
 * Day 02 (Month 03) DSA: Advanced Backtracking Patterns
 * - LeetCode 51: N-Queens (Hard)
 * - LeetCode 79: Word Search (Matrix DFS Backtracking)
 * - LeetCode 46: Permutations
 */
public class BacktrackingAdvanced {

    // -------------------------------------------------------------
    // LC 51: N-Queens
    // -------------------------------------------------------------
    public static List<List<String>> solveNQueens(int n) {
        List<List<String>> results = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');

        Set<Integer> cols = new HashSet<>();
        Set<Integer> diag1 = new HashSet<>(); // (r - c)
        Set<Integer> diag2 = new HashSet<>(); // (r + c)

        backtrackNQueens(0, n, board, cols, diag1, diag2, results);
        return results;
    }

    private static void backtrackNQueens(
        int row, int n, char[][] board,
        Set<Integer> cols, Set<Integer> diag1, Set<Integer> diag2,
        List<List<String>> results
    ) {
        if (row == n) {
            List<String> solution = new ArrayList<>();
            for (char[] r : board) solution.add(new String(r));
            results.add(solution);
            return;
        }

        for (int col = 0; col < n; col++) {
            if (cols.contains(col) || diag1.contains(row - col) || diag2.contains(row + col)) {
                continue;
            }

            // Place queen
            board[row][col] = 'Q';
            cols.add(col);
            diag1.add(row - col);
            diag2.add(row + col);

            backtrackNQueens(row + 1, n, board, cols, diag1, diag2, results);

            // Backtrack
            board[row][col] = '.';
            cols.remove(col);
            diag1.remove(row - col);
            diag2.remove(row + col);
        }
    }

    // -------------------------------------------------------------
    // LC 79: Word Search
    // -------------------------------------------------------------
    public static boolean exist(char[][] board, String word) {
        int m = board.length, n = board[0].length;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (dfsWordSearch(board, word, 0, r, c)) {
                    return true;
                }
            }
        }
        return false;
    }

    private static boolean dfsWordSearch(char[][] board, String word, int idx, int r, int c) {
        if (idx == word.length()) return true;
        if (r < 0 || r >= board.length || c < 0 || c >= board[0].length || board[r][c] != word.charAt(idx)) {
            return false;
        }

        char original = board[r][c];
        board[r][c] = '#'; // Mark visited

        boolean found = dfsWordSearch(board, word, idx + 1, r + 1, c) ||
                        dfsWordSearch(board, word, idx + 1, r - 1, c) ||
                        dfsWordSearch(board, word, idx + 1, r, c + 1) ||
                        dfsWordSearch(board, word, idx + 1, r, c - 1);

        board[r][c] = original; // Backtrack
        return found;
    }

    // -------------------------------------------------------------
    // LC 46: Permutations
    // -------------------------------------------------------------
    public static List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrackPermute(nums, new ArrayList<>(), new boolean[nums.length], result);
        return result;
    }

    private static void backtrackPermute(int[] nums, List<Integer> current, boolean[] used, List<List<Integer>> result) {
        if (current.size() == nums.length) {
            result.add(new ArrayList<>(current));
            return;
        }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            current.add(nums[i]);

            backtrackPermute(nums, current, used, result);

            used[i] = false;
            current.remove(current.size() - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Month 03 Day 02: Advanced Backtracking DSA Suite");
        System.out.println("==================================================");

        // Test 1: LC 51 N-Queens
        List<List<String>> nQueens4 = solveNQueens(4);
        System.out.println("LC 51 (4-Queens Solutions Count): " + nQueens4.size());
        assert nQueens4.size() == 2 : "LC 51 Failed";

        // Test 2: LC 79 Word Search
        char[][] board = {
            {'A', 'B', 'C', 'E'},
            {'S', 'F', 'C', 'S'},
            {'A', 'D', 'E', 'E'}
        };
        boolean existsABCCED = exist(board, "ABCCED");
        System.out.println("LC 79 Word 'ABCCED' Exists: " + existsABCCED);
        assert existsABCCED : "LC 79 Failed";

        // Test 3: LC 46 Permutations
        int[] nums = {1, 2, 3};
        List<List<Integer>> perms = permute(nums);
        System.out.println("LC 46 Permutations Count of [1,2,3]: " + perms.size());
        assert perms.size() == 6 : "LC 46 Failed";

        System.out.println("\nAll Java Backtracking tests executed successfully! [OK]");
    }
}
