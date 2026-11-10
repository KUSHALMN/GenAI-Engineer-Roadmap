package Month07.Day30;

import java.util.HashMap;
import java.util.Map;

/**
 * Capstone Production DSA Review:
 * Trie-based prefix autocomplete search with O(L) lookup complexity.
 */
public class CapstoneProductionDsaReview {

    public static class TrieNode {
        Map<Character, TrieNode> children = new HashMap<>();
        boolean isEndOfWord = false;
    }

    public static class AutocompleteTrie {
        private final TrieNode root = new TrieNode();

        public void insert(String word) {
            TrieNode current = root;
            for (char ch : word.toCharArray()) {
                current = current.children.computeIfAbsent(ch, c -> new TrieNode());
            }
            current.isEndOfWord = true;
        }

        public boolean startsWith(String prefix) {
            TrieNode current = root;
            for (char ch : prefix.toCharArray()) {
                current = current.children.get(ch);
                if (current == null) return false;
            }
            return true;
        }
    }

    public static void main(String[] args) {
        AutocompleteTrie trie = new AutocompleteTrie();
        trie.insert("kubernetes");
        trie.insert("kubeflow");

        assert trie.startsWith("kube");
        assert !trie.startsWith("docker");

        System.out.println("Day 30 Capstone Production DSA Review verification passed.");
    }
}
