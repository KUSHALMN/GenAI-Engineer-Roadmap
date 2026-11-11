package Month_08.Day_19.DSA;

/**
 * Day 19: Timed DSA Problem Set — Trie & Bit Manipulation.
 * Focus: LeetCode 208 (Implement Trie) & LeetCode 136 (Single Number).
 */
public class TrieBitManipulationTimedSet {

    // LeetCode 208: Prefix Tree (Trie)
    public static class Trie {
        private static class TrieNode {
            TrieNode[] children = new TrieNode[26];
            boolean isEnd = false;
        }

        private final TrieNode root;

        public Trie() {
            root = new TrieNode();
        }

        public void insert(String word) {
            TrieNode node = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (node.children[idx] == null) {
                    node.children[idx] = new TrieNode();
                }
                node = node.children[idx];
            }
            node.isEnd = true;
        }

        public boolean search(String word) {
            TrieNode node = getNode(word);
            return node != null && node.isEnd;
        }

        public boolean startsWith(String prefix) {
            return getNode(prefix) != null;
        }

        private TrieNode getNode(String str) {
            TrieNode node = root;
            for (char c : str.toCharArray()) {
                int idx = c - 'a';
                if (node.children[idx] == null) return null;
                node = node.children[idx];
            }
            return node;
        }
    }

    // LeetCode 136: Single Number - O(N) Time, O(1) Space using XOR
    public static int singleNumber(int[] nums) {
        int result = 0;
        for (int num : nums) {
            result ^= num;
        }
        return result;
    }

    public static void main(String[] args) {
        // Trie tests
        Trie trie = new Trie();
        trie.insert("apple");
        assert trie.search("apple") : "Trie search apple failed";
        assert !trie.search("app") : "Trie search app failed";
        assert trie.startsWith("app") : "Trie startsWith app failed";
        trie.insert("app");
        assert trie.search("app") : "Trie search app post-insert failed";

        // LC 136 tests
        assert singleNumber(new int[]{2, 2, 1}) == 1 : "XOR Test 1 Failed";
        assert singleNumber(new int[]{4, 1, 2, 1, 2}) == 4 : "XOR Test 2 Failed";
        assert singleNumber(new int[]{1}) == 1 : "XOR Test 3 Failed";

        System.out.println("Day 19 Trie & Bit Manipulation Timed Set verification passed.");
    }
}
