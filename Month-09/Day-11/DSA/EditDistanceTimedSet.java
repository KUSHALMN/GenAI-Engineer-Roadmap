package Month_09.Day_11.DSA;

/**
 * Day 11: Timed DSA Problem Set — Dynamic Programming Edit Distance.
 * Focus: LeetCode 72 (Edit Distance) - O(M * N) Time, O(min(M, N)) Space Optimization.
 */
public class EditDistanceTimedSet {

    // LeetCode 72: Edit Distance with 1D Array Space Optimization
    public static int minDistance(String word1, String word2) {
        if (word1 == null || word2 == null) return 0;
        int m = word1.length();
        int n = word2.length();

        if (m < n) {
            return minDistance(word2, word1); // Ensure n is smaller to minimize space O(min(M, N))
        }

        int[] dp = new int[n + 1];
        for (int j = 0; j <= n; j++) {
            dp[j] = j; // Base case: inserting j characters into empty string
        }

        for (int i = 1; i <= m; i++) {
            int prevDiag = dp[0];
            dp[0] = i; // Base case: deleting i characters
            for (int j = 1; j <= n; j++) {
                int temp = dp[j];
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[j] = prevDiag;
                } else {
                    int insertOp = dp[j - 1];
                    int deleteOp = dp[j];
                    int replaceOp = prevDiag;
                    dp[j] = 1 + Math.min(replaceOp, Math.min(insertOp, deleteOp));
                }
                prevDiag = temp;
            }
        }
        return dp[n];
    }

    public static void main(String[] args) {
        assert minDistance("horse", "ros") == 3 : "Test 1 Failed: horse -> ros";
        assert minDistance("intention", "execution") == 5 : "Test 2 Failed: intention -> execution";
        assert minDistance("", "abc") == 3 : "Test 3 Failed: empty -> abc";
        assert minDistance("abc", "") == 3 : "Test 4 Failed: abc -> empty";
        assert minDistance("same", "same") == 0 : "Test 5 Failed: identical words";

        System.out.println("Day 11 Edit Distance Timed Set verification passed.");
    }
}
