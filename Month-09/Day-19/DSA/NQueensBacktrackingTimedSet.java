package Month_09.Day_19.DSA;

/**
 * Day 19: Timed DSA Problem Set — N-Queens Backtracking with Bitmasking.
 * Focus: LeetCode 52 (N-Queens II) - O(N!) Time, O(N) Space Bitmask Optimization.
 */
public class NQueensBacktrackingTimedSet {

    public static int totalNQueens(int n) {
        if (n <= 0) return 0;
        return solve(0, n, 0, 0, 0);
    }

    private static int solve(int row, int n, int cols, int diag1, int diag2) {
        if (row == n) return 1;

        int count = 0;
        // Available positions in this row are bits that are 0 in all three bitmasks
        int available = ((1 << n) - 1) & ~(cols | diag1 | diag2);

        while (available != 0) {
            // Extract the lowest set bit (position for next queen)
            int p = available & (-available);
            // Place queen and recurse to next row
            count += solve(row + 1, n, cols | p, (diag1 | p) << 1, (diag2 | p) >> 1);
            // Clear the lowest set bit
            available &= available - 1;
        }
        return count;
    }

    public static void main(String[] args) {
        assert totalNQueens(4) == 2 : "N=4 Failed: expected 2";
        assert totalNQueens(1) == 1 : "N=1 Failed: expected 1";
        assert totalNQueens(8) == 92 : "N=8 Failed: expected 92";
        assert totalNQueens(9) == 352 : "N=9 Failed: expected 352";

        System.out.println("Day 19 N-Queens Backtracking Timed Set verification passed.");
    }
}
