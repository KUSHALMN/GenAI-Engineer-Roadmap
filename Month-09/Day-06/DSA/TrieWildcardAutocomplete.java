package Month_09.Day_06.DSA;

/**
 * Day 06: Timed DSA Problem Set — Trie with Wildcard Matching.
 * Focus: LeetCode 211 (Design Add and Search Words Data Structure) - DFS Backtracking on Trie.
 */
public class TrieWildcardAutocomplete {

    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }

    private final TrieNode root;

    public TrieWildcardAutocomplete() {
        this.root = new TrieNode();
    }

    public void addWord(String word) {
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

    public boolean search(String word) {
        return searchHelper(word, 0, root);
    }

    private boolean searchHelper(String word, int idx, TrieNode node) {
        if (node == null) return false;
        if (idx == word.length()) return node.isEnd;

        char c = word.charAt(idx);
        if (c == '.') {
            // Wildcard: explore all 26 possible branches
            for (int i = 0; i < 26; i++) {
                if (node.children[i] != null) {
                    if (searchHelper(word, idx + 1, node.children[i])) {
                        return true;
                    }
                }
            }
            return false;
        } else {
            return searchHelper(word, idx + 1, node.children[c - 'a']);
        }
    }

    public static void main(String[] args) {
        TrieWildcardAutocomplete dict = new TrieWildcardAutocomplete();
        dict.addWord("bad");
        dict.addWord("dad");
        dict.addWord("mad");

        assert !dict.search("pad") : "Search 'pad' failed";
        assert dict.search("bad") : "Search 'bad' failed";
        assert dict.search(".ad") : "Search '.ad' failed";
        assert dict.search("b..") : "Search 'b..' failed";
        assert !dict.search("b...") : "Search 'b...' failed";

        System.out.println("Day 06 Trie Wildcard Autocomplete verification passed.");
    }
}
