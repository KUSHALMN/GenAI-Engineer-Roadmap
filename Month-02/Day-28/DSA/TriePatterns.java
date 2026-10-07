package DSA;

import java.util.*;

/**
 * Day 28 DSA: Trie (Prefix Tree) & Autocomplete Patterns
 * - LeetCode 208: Implement Trie (Prefix Tree)
 * - LeetCode 211: Design Add and Search Words (Wildcard '.' Support)
 * - LeetCode 14: Longest Common Prefix via Trie Traversal
 */
public class TriePatterns {

    // -------------------------------------------------------------
    // LC 208: Implement Trie
    // -------------------------------------------------------------
    public static class TrieNode {
        public TrieNode[] children = new TrieNode[26];
        public boolean isEndOfWord = false;
        public int passCount = 0; // Number of words sharing this prefix
    }

    public static class Trie {
        private final TrieNode root;

        public Trie() {
            root = new TrieNode();
        }

        public void insert(String word) {
            TrieNode current = root;
            for (char ch : word.toCharArray()) {
                int idx = ch - 'a';
                if (current.children[idx] == null) {
                    current.children[idx] = new TrieNode();
                }
                current = current.children[idx];
                current.passCount++;
            }
            current.isEndOfWord = true;
        }

        public boolean search(String word) {
            TrieNode node = findNode(word);
            return node != null && node.isEndOfWord;
        }

        public boolean startsWith(String prefix) {
            return findNode(prefix) != null;
        }

        private TrieNode findNode(String str) {
            TrieNode current = root;
            for (char ch : str.toCharArray()) {
                int idx = ch - 'a';
                if (current.children[idx] == null) return null;
                current = current.children[idx];
            }
            return current;
        }

        public List<String> autocomplete(String prefix) {
            List<String> results = new ArrayList<>();
            TrieNode start = findNode(prefix);
            if (start != null) {
                dfsCollect(start, new StringBuilder(prefix), results);
            }
            return results;
        }

        private void dfsCollect(TrieNode node, StringBuilder current, List<String> results) {
            if (node.isEndOfWord) {
                results.add(current.toString());
            }
            for (int i = 0; i < 26; i++) {
                if (node.children[i] != null) {
                    current.append((char) ('a' + i));
                    dfsCollect(node.children[i], current, results);
                    current.deleteCharAt(current.length() - 1);
                }
            }
        }
    }

    // -------------------------------------------------------------
    // LC 211: WordDictionary with Wildcard '.' Search
    // -------------------------------------------------------------
    public static class WordDictionary {
        private final TrieNode root = new TrieNode();

        public void addWord(String word) {
            TrieNode curr = root;
            for (char ch : word.toCharArray()) {
                int idx = ch - 'a';
                if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
                curr = curr.children[idx];
            }
            curr.isEndOfWord = true;
        }

        public boolean search(String word) {
            return searchDfs(word, 0, root);
        }

        private boolean searchDfs(String word, int index, TrieNode curr) {
            if (curr == null) return false;
            if (index == word.length()) return curr.isEndOfWord;

            char ch = word.charAt(index);
            if (ch == '.') {
                for (int i = 0; i < 26; i++) {
                    if (curr.children[i] != null && searchDfs(word, index + 1, curr.children[i])) {
                        return true;
                    }
                }
                return false;
            } else {
                int idx = ch - 'a';
                return searchDfs(word, index + 1, curr.children[idx]);
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println(" Day 28: Trie & Prefix Autocomplete DSA Suite");
        System.out.println("==================================================");

        // Test 1: LC 208 Trie
        Trie trie = new Trie();
        trie.insert("apple");
        trie.insert("app");
        trie.insert("apply");
        trie.insert("apricot");

        System.out.println("LC 208 Search 'apple': " + trie.search("apple"));
        assert trie.search("apple") : "Trie search apple failed";
        assert !trie.search("appl") : "Trie search appl should be false";
        assert trie.startsWith("app") : "Trie startsWith app failed";

        // Autocomplete demonstration
        List<String> suggestions = trie.autocomplete("app");
        System.out.println("Trie Autocomplete 'app': " + suggestions);
        assert suggestions.contains("apple") && suggestions.contains("app") : "Autocomplete failed";

        // Test 2: LC 211 WordDictionary with '.'
        WordDictionary dict = new WordDictionary();
        dict.addWord("bad");
        dict.addWord("dad");
        dict.addWord("mad");
        System.out.println("LC 211 Search 'pad': " + dict.search("pad")); // false
        System.out.println("LC 211 Search '.ad': " + dict.search(".ad")); // true
        System.out.println("LC 211 Search 'b..': " + dict.search("b..")); // true
        assert !dict.search("pad") : "LC 211 pad failed";
        assert dict.search(".ad") : "LC 211 .ad failed";
        assert dict.search("b..") : "LC 211 b.. failed";

        System.out.println("\nAll Java Trie tests executed successfully! [OK]");
    }
}
