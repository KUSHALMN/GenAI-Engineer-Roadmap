import java.util.*;

/**
 * Day 28: Trie + Backtracking — Word Search II (Full Robust Implementation)
 * Problem: Given an m x n board of characters and a list of strings words, return all words on the board.
 *
 * Algorithm:
 * - Insert words into Trie.
 * - For each cell, traverse Trie and board concurrently.
 * - Backtrack and prune matched leaf nodes.
 *
 * Time Complexity: O(M * N * 4 * 3^(L-1))
 * Space Complexity: O(Sum of word lengths)
 */
public class WordSearchTwo {

    static class TrieNode {
        TrieNode[] next = new TrieNode[26];
        String word;
    }

    public List<String> findWords(char[][] board, String[] words) {
        List<String> res = new ArrayList<>();
        TrieNode root = buildTrie(words);

        for (int r = 0; r < board.length; r++) {
            for (int c = 0; c < board[0].length; c++) {
                dfs(board, r, c, root, res);
            }
        }
        return res;
    }

    private void dfs(char[][] board, int r, int c, TrieNode p, List<String> res) {
        char ch = board[r][c];
        if (ch == '#' || p.next[ch - 'a'] == null) return;
        p = p.next[ch - 'a'];

        if (p.word != null) {
            res.add(p.word);
            p.word = null; // De-duplicate
        }

        board[r][c] = '#';
        if (r > 0) dfs(board, r - 1, c, p, res);
        if (c > 0) dfs(board, r, c - 1, p, res);
        if (r < board.length - 1) dfs(board, r + 1, c, p, res);
        if (c < board[0].length - 1) dfs(board, r, c + 1, p, res);
        board[r][c] = ch; // Backtrack
    }

    private TrieNode buildTrie(String[] words) {
        TrieNode root = new TrieNode();
        for (String w : words) {
            TrieNode curr = root;
            for (char ch : w.toCharArray()) {
                int idx = ch - 'a';
                if (curr.next[idx] == null) curr.next[idx] = new TrieNode();
                curr = curr.next[idx];
            }
            curr.word = w;
        }
        return root;
    }

    public static void main(String[] args) {
        WordSearchTwo solver = new WordSearchTwo();
        char[][] board = {
            {'a','b'},
            {'c','d'}
        };
        String[] words = {"ab", "cb", "ad", "bd", "acdb"};
        List<String> found = solver.findWords(board, words);

        System.out.println("Found words: " + found);
        assert found.contains("ab") && found.contains("acdb");
        System.out.println("Day 28 DSA WordSearchTwo verification passed!");
    }
}
