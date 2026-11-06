import java.util.*;

/**
 * Day 07: Trie + Backtracking — Word Search II
 * Problem: Given an m x n board of characters and a list of strings words, return all words on the board.
 *
 * Algorithm:
 * - Insert all words into a Prefix Trie.
 * - DFS from each cell; prune branch immediately if current prefix is not in Trie.
 * - Optimization: Remove matched word from Trie node to avoid duplicate additions.
 *
 * Time Complexity: O(m * n * 4 * 3^(L-1)) where L is max word length.
 * Space Complexity: O(Total characters in words) for Trie.
 */
public class WordSearchTrie {

    static class TrieNode {
        Map<Character, TrieNode> children = new HashMap<>();
        String word = null;
    }

    private TrieNode buildTrie(String[] words) {
        TrieNode root = new TrieNode();
        for (String w : words) {
            TrieNode curr = root;
            for (char c : w.toCharArray()) {
                curr.children.putIfAbsent(c, new TrieNode());
                curr = curr.children.get(c);
            }
            curr.word = w; // Store complete word at leaf
        }
        return root;
    }

    public List<String> findWords(char[][] board, String[] words) {
        List<String> result = new ArrayList<>();
        TrieNode root = buildTrie(words);

        for (int r = 0; r < board.length; r++) {
            for (int c = 0; c < board[0].length; c++) {
                if (root.children.containsKey(board[r][c])) {
                    dfs(board, r, c, root, result);
                }
            }
        }
        return result;
    }

    private void dfs(char[][] board, int r, int c, TrieNode parent, List<String> result) {
        char letter = board[r][c];
        TrieNode curr = parent.children.get(letter);
        if (curr == null) return;

        if (curr.word != null) {
            result.add(curr.word);
            curr.word = null; // Avoid duplicate collection
        }

        board[r][c] = '#'; // Mark visited
        int[] dr = {-1, 1, 0, 0};
        int[] dc = {0, 0, -1, 1};

        for (int i = 0; i < 4; i++) {
            int nr = r + dr[i];
            int nc = c + dc[i];
            if (nr >= 0 && nr < board.length && nc >= 0 && nc < board[0].length && board[nr][nc] != '#') {
                dfs(board, nr, nc, curr, result);
            }
        }

        board[r][c] = letter; // Backtrack
    }

    public static void main(String[] args) {
        WordSearchTrie solver = new WordSearchTrie();
        char[][] board = {
            {'o','a','a','n'},
            {'e','t','a','e'},
            {'i','h','k','r'},
            {'i','f','l','v'}
        };
        String[] words = {"oath","pea","eat","rain"};
        List<String> found = solver.findWords(board, words);

        System.out.println("Found words in board: " + found);
        assert found.contains("oath") && found.contains("eat");
        assert !found.contains("pea");
        System.out.println("Day 07 DSA WordSearchTrie verification passed!");
    }
}
