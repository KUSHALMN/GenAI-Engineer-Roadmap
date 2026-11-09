import java.util.*;

public class TrieApplicationsRevision {
    public static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEndOfWord = false;
    }

    private static final TrieNode root = new TrieNode();

    public static void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
            curr = curr.children[idx];
        }
        curr.isEndOfWord = true;
    }

    public static boolean search(String word) {
        TrieNode node = getNode(word);
        return node != null && node.isEndOfWord;
    }

    public static boolean startsWith(String prefix) {
        return getNode(prefix) != null;
    }

    private static TrieNode getNode(String str) {
        TrieNode curr = root;
        for (char c : str.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) return null;
            curr = curr.children[idx];
        }
        return curr;
    }

    public static void main(String[] args) {
        System.out.println("=== Trie Applications Verification ===");
        insert("multimodal");
        insert("multiagent");
        assert search("multimodal") : "Search failed";
        assert !search("multi") : "Search prefix as word failed";
        assert startsWith("multi") : "StartsWith failed";
        System.out.println("Trie insert/search/startsWith passed successfully!");
    }
}
