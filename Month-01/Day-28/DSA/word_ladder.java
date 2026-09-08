import java.util.*;

/**
 * Problem: Word Ladder (LeetCode 127 - Hard / High Frequency FAANG)
 * 
 * A transformation sequence from word beginWord to word endWord using a dictionary wordList
 * is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
 * - Every adjacent pair of words differs by exactly one letter.
 * - Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
 * - sk == endWord
 * 
 * Given two words, beginWord and endWord, and a dictionary wordList, return the number of words
 * in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.
 * 
 * Optimal Approach: Bidirectional Breadth-First Search (BFS)
 * - Standard BFS expands from beginWord with branching factor b up to depth d => O(b^d).
 * - Bidirectional BFS expands simultaneously from beginWord (forward) and endWord (backward).
 * - Search space shrinks to 2 * O(b^(d/2)), dramatically reducing time and memory.
 * - Always expand the smaller frontier set at each step to maintain minimal branching.
 * 
 * Complexity:
 * - Time Complexity: O(M^2 * N) where M is word length, N is dictionary size.
 * - Space Complexity: O(M * N) for the dictionary hash set and frontier sets.
 */
public class word_ladder {

    // ==========================================
    // Approach: Bidirectional BFS (Optimal)
    // ==========================================
    public static int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> dict = new HashSet<>(wordList);
        if (!dict.contains(endWord)) {
            return 0;
        }

        Set<String> forwardSet = new HashSet<>();
        Set<String> backwardSet = new HashSet<>();
        Set<String> visited = new HashSet<>();

        forwardSet.add(beginWord);
        backwardSet.add(endWord);
        visited.add(beginWord);
        visited.add(endWord);

        int step = 1;

        while (!forwardSet.isEmpty() && !backwardSet.isEmpty()) {
            // Always expand the smaller set for optimal branch pruning
            if (forwardSet.size() > backwardSet.size()) {
                Set<String> temp = forwardSet;
                forwardSet = backwardSet;
                backwardSet = temp;
            }

            Set<String> nextLevel = new HashSet<>();

            for (String word : forwardSet) {
                char[] chars = word.toCharArray();

                for (int i = 0; i < chars.length; i++) {
                    char originalChar = chars[i];

                    for (char c = 'a'; c <= 'z'; c++) {
                        if (c == originalChar) continue;
                        chars[i] = c;
                        String candidate = new String(chars);

                        // If the candidate is found in the opposite frontier, paths have met!
                        if (backwardSet.contains(candidate)) {
                            return step + 1;
                        }

                        if (dict.contains(candidate) && !visited.contains(candidate)) {
                            nextLevel.add(candidate);
                            visited.add(candidate);
                        }
                    }

                    chars[i] = originalChar; // Backtrack
                }
            }

            forwardSet = nextLevel;
            step++;
        }

        return 0; // No valid path found
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 127: Word Ladder (Java)");
        System.out.println("=================================================");

        // Test 1: Standard transformation
        String begin1 = "hit";
        String end1 = "cog";
        List<String> dict1 = Arrays.asList("hot", "dot", "dog", "lot", "log", "cog");
        int res1 = ladderLength(begin1, end1, dict1);
        System.out.println("Test 1 ('hit' -> 'cog') -> Expected 5: " + res1);
        assert res1 == 5 : "Failed Test 1 (Expected 5)";

        // Test 2: endWord not in dictionary
        String begin2 = "hit";
        String end2 = "cog";
        List<String> dict2 = Arrays.asList("hot", "dot", "dog", "lot", "log");
        int res2 = ladderLength(begin2, end2, dict2);
        System.out.println("Test 2 ('cog' not in dict) -> Expected 0: " + res2);
        assert res2 == 0 : "Failed Test 2";

        // Test 3: Direct 1-character transition
        String begin3 = "hit";
        String end3 = "hot";
        List<String> dict3 = Arrays.asList("hot");
        int res3 = ladderLength(begin3, end3, dict3);
        System.out.println("Test 3 ('hit' -> 'hot') -> Expected 2: " + res3);
        assert res3 == 2 : "Failed Test 3";

        System.out.println("\n✅ All Word Ladder test cases passed successfully!");
    }
}
