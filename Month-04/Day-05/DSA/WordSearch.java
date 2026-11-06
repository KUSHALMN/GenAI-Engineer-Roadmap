import java.util.*;

/**
 * Day 05: Grid Backtracking — Word Search
 * Problem: Given an m x n grid of characters board and a string word, return true if word exists in the grid.
 * The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically).
 * The same letter cell may not be used more than once.
 *
 * Time Complexity: O(m * n * 3^L) where L is word length (3 choices after first cell)
 * Space Complexity: O(L) for recursion stack.
 */
public class WordSearch {

    public boolean exist(char[][] board, String word) {
        int m = board.length;
        int n = board[0].length;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (board[r][c] == word.charAt(0) && dfs(board, r, c, word, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean dfs(char[][] board, int r, int c, String word, int idx) {
        if (idx == word.length()) return true;

        if (r < 0 || r >= board.length || c < 0 || c >= board[0].length || board[r][c] != word.charAt(idx)) {
            return false;
        }

        // Mark in-place visited
        char temp = board[r][c];
        board[r][c] = '#';

        boolean found = dfs(board, r + 1, c, word, idx + 1) ||
                        dfs(board, r - 1, c, word, idx + 1) ||
                        dfs(board, r, c + 1, word, idx + 1) ||
                        dfs(board, r, c - 1, word, idx + 1);

        // Restore state (backtrack)
        board[r][c] = temp;
        return found;
    }

    public static void main(String[] args) {
        WordSearch solver = new WordSearch();
        char[][] board = {
            {'A', 'B', 'C', 'E'},
            {'S', 'F', 'C', 'S'},
            {'A', 'D', 'E', 'E'}
        };

        assert solver.exist(board, "ABCCED") : "Word 'ABCCED' must exist";
        assert solver.exist(board, "SEE") : "Word 'SEE' must exist";
        assert !solver.exist(board, "ABCB") : "Word 'ABCB' must not exist";

        System.out.println("Day 05 DSA WordSearch verification passed!");
    }
}
