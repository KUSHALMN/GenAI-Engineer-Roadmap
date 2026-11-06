import java.util.*;

/**
 * Day 06: Constraint Backtracking — N-Queens
 * Problem: The n-queens puzzle is the problem of placing n queens on an n x n chessboard
 * such that no two queens attack each other.
 *
 * Algorithm:
 * - Backtrack row by row.
 * - Use boolean sets/arrays to track attacked columns, diagonal (r - c), and anti-diagonal (r + c) in O(1).
 *
 * Time Complexity: O(n!)
 * Space Complexity: O(n) for state arrays and recursion stack.
 */
public class NQueens {

    public List<List<String>> solveNQueens(int n) {
        List<List<String>> solutions = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');

        boolean[] cols = new boolean[n];
        boolean[] diag1 = new boolean[2 * n]; // r - c + n
        boolean[] diag2 = new boolean[2 * n]; // r + c

        backtrack(0, n, board, cols, diag1, diag2, solutions);
        return solutions;
    }

    private void backtrack(int r, int n, char[][] board, boolean[] cols, boolean[] diag1, boolean[] diag2, List<List<String>> solutions) {
        if (r == n) {
            List<String> currentBoard = new ArrayList<>();
            for (char[] row : board) currentBoard.add(new String(row));
            solutions.add(currentBoard);
            return;
        }

        for (int c = 0; c < n; c++) {
            int d1 = r - c + n;
            int d2 = r + c;
            if (cols[c] || diag1[d1] || diag2[d2]) continue;

            board[r][c] = 'Q';
            cols[c] = diag1[d1] = diag2[d2] = true;

            backtrack(r + 1, n, board, cols, diag1, diag2, solutions);

            board[r][c] = '.';
            cols[c] = diag1[d1] = diag2[d2] = false;
        }
    }

    public static void main(String[] args) {
        NQueens solver = new NQueens();
        List<List<String>> res4 = solver.solveNQueens(4);

        System.out.println("4-Queens solutions count: " + res4.size());
        assert res4.size() == 2 : "4-Queens should have exactly 2 solutions";
        System.out.println("Day 06 DSA NQueens verification passed!");
    }
}
