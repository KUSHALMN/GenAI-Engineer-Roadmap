import java.util.*;

/**
 * Problem: Word Break (LeetCode 139 - Medium / High-Frequency FAANG)
 * 
 * Given a string s and a dictionary of strings wordDict, return true if s can be
 * segmented into a space-separated sequence of one or more dictionary words.
 * 
 * Note that the same word in the dictionary may be reused multiple times in the segmentation.
 * 
 * Approaches:
 * 1. Bottom-Up Dynamic Programming:
 *    - dp[i] = true if s[0...i-1] can be segmented into words in wordDict.
 *    - Transition: dp[i] = true if for any j < i, dp[j] == true and s.substring(j, i) in wordDict.
 *    - Optimization: Prune inner loop based on max word length in wordDict.
 *    - Time Complexity: O(n * L * L) where n = s.length(), L = max word length.
 *    - Space Complexity: O(n + W) where W is the total characters in wordDict for HashSet.
 * 
 * 2. Trie + Memoization / DP:
 *    - Avoid substring allocations by traversing characters in a Prefix Tree (Trie).
 */
public class word_break {

    // ==========================================
    // Approach 1: Optimized Dynamic Programming
    // ==========================================
    public static boolean wordBreak(String s, List<String> wordDict) {
        if (s == null || s.isEmpty() || wordDict == null || wordDict.isEmpty()) {
            return false;
        }

        Set<String> dict = new HashSet<>(wordDict);
        int maxLen = 0;
        for (String word : wordDict) {
            maxLen = Math.max(maxLen, word.length());
        }

        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true; // Base case: empty prefix is valid

        for (int i = 1; i <= n; i++) {
            // Only look back up to max word length
            int start = Math.max(0, i - maxLen);
            for (int j = i - 1; j >= start; j--) {
                if (dp[j] && dict.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break; // Early exit once a valid split is confirmed
                }
            }
        }

        return dp[n];
    }

    // ==========================================
    // Approach 2: Trie-based Segmentation
    // ==========================================
    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }

    public static boolean wordBreakTrie(String s, List<String> wordDict) {
        TrieNode root = new TrieNode();
        for (String word : wordDict) {
            TrieNode curr = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) {
                    curr.children[idx] = new TrieNode();
                }
                curr = curr.children[idx];
            }
            curr.isEnd = true;
        }

        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;

        for (int i = 0; i < n; i++) {
            if (!dp[i]) continue;

            TrieNode curr = root;
            for (int j = i; j < n; j++) {
                int idx = s.charAt(j) - 'a';
                if (curr.children[idx] == null) {
                    break; // Prefix not in Trie
                }
                curr = curr.children[idx];
                if (curr.isEnd) {
                    dp[j + 1] = true;
                }
            }
        }

        return dp[n];
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 139: Word Break (Java)");
        System.out.println("=================================================");

        // Test 1: Standard case
        String s1 = "leetcode";
        List<String> d1 = Arrays.asList("leet", "code");
        boolean res1 = wordBreak(s1, d1);
        boolean res1Trie = wordBreakTrie(s1, d1);
        System.out.println("Test 1 ('leetcode', ['leet', 'code']) -> Expected true: " + res1 + " (Trie: " + res1Trie + ")");
        assert res1 && res1Trie : "Failed Test 1";

        // Test 2: Word reuse
        String s2 = "applepenapple";
        List<String> d2 = Arrays.asList("apple", "pen");
        boolean res2 = wordBreak(s2, d2);
        boolean res2Trie = wordBreakTrie(s2, d2);
        System.out.println("Test 2 ('applepenapple', ['apple', 'pen']) -> Expected true: " + res2);
        assert res2 && res2Trie : "Failed Test 2";

        // Test 3: Cannot segment
        String s3 = "catsandog";
        List<String> d3 = Arrays.asList("cats", "dog", "sand", "and", "cat");
        boolean res3 = wordBreak(s3, d3);
        boolean res3Trie = wordBreakTrie(s3, d3);
        System.out.println("Test 3 ('catsandog') -> Expected false: " + res3);
        assert !res3 && !res3Trie : "Failed Test 3";

        // Test 4: Single char segmentation
        String s4 = "aaaaaaa";
        List<String> d4 = Arrays.asList("aaaa", "aaa");
        boolean res4 = wordBreak(s4, d4);
        System.out.println("Test 4 ('aaaaaaa', ['aaaa', 'aaa']) -> Expected true: " + res4);
        assert res4 : "Failed Test 4";

        System.out.println("\n✅ All Word Break test cases passed successfully!");
    }
}
