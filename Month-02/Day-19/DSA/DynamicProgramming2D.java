import java.util.HashMap;
import java.util.Map;

/**
 * 2D Dynamic Programming & Trie in Java
 *
 * Problems Covered:
 *   1. 0/1 Knapsack Problem -> O(N * W) time, O(W) space
 *   2. LeetCode 1143 - Longest Common Subsequence -> O(M * N) time, O(M * N) space
 *   3. LeetCode 208  - Implement Trie (Prefix Tree) -> O(L) time per operation
 */
public class DynamicProgramming2D {

    /**
     * Classic 0/1 Knapsack: Bottom-up 1D space optimized
     */
    public int knapsack01(int[] weights, int[] values, int capacity) {
        int n = weights.length;
        int[] dp = new int[capacity + 1];

        for (int i = 0; i < n; i++) {
            int w = weights[i];
            int v = values[i];
            for (int cap = capacity; cap >= w; cap--) {
                dp[cap] = Math.max(dp[cap], dp[cap - w] + v);
            }
        }
        return dp[capacity];
    }

    /**
     * LC 1143: Longest Common Subsequence
     */
    public int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length();
        int n = text2.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[m][n];
    }

    /**
     * LC 208: Trie (Prefix Tree)
     */
    public static class Trie {
        private static class TrieNode {
            Map<Character, TrieNode> children = new HashMap<>();
            boolean isEnd = false;
        }

        private final TrieNode root = new TrieNode();

        public void insert(String word) {
            TrieNode curr = root;
            for (char ch : word.toCharArray()) {
                curr.children.putIfAbsent(ch, new TrieNode());
                curr = curr.children.get(ch);
            }
            curr.isEnd = true;
        }

        public boolean search(String word) {
            TrieNode node = findPrefixNode(word);
            return node != null && node.isEnd;
        }

        public boolean startsWith(String prefix) {
            return findPrefixNode(prefix) != null;
        }

        private TrieNode findPrefixNode(String prefix) {
            TrieNode curr = root;
            for (char ch : prefix.toCharArray()) {
                if (!curr.children.containsKey(ch)) return null;
                curr = curr.children.get(ch);
            }
            return curr;
        }
    }

    public static void main(String[] args) {
        DynamicProgramming2D dp2 = new DynamicProgramming2D();

        // 1. 0/1 Knapsack
        int[] weights = {1, 2, 3};
        int[] values = {60, 100, 120};
        int maxVal = dp2.knapsack01(weights, values, 5);
        System.out.println("0/1 Knapsack Max Value: " + maxVal); // 220

        // 2. LC 1143 LCS
        int lcs = dp2.longestCommonSubsequence("abcde", "ace");
        System.out.println("LC 1143 LCS (abcde, ace): " + lcs); // 3

        // 3. LC 208 Trie
        Trie trie = new Trie();
        trie.insert("apple");
        System.out.println("Trie Search 'apple': " + trie.search("apple"));   // true
        System.out.println("Trie Search 'app': " + trie.search("app"));       // false
        System.out.println("Trie StartsWith 'app': " + trie.startsWith("app")); // true
    }
}
