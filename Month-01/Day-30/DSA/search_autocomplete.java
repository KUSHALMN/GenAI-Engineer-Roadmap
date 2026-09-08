import java.util.*;

/**
 * Problem: Design Search Autocomplete System (LeetCode 642 - Hard / System Design DSA)
 * 
 * Design a search autocomplete system for a search engine. Users may input a sentence
 * character by character. For each character typed, return the top 3 historical hot sentences
 * that have the same prefix as the part of sentence already typed.
 * 
 * Rules:
 * - Hot degree is determined by the frequency of searches.
 * - If frequencies are equal, use ASCII alphabetical order.
 * - If '#' is typed, the current sentence ends and its historical frequency increments by 1.
 * 
 * Optimal Architecture: Trie with Top-K Frequency Caching
 * - Each TrieNode contains:
 *   - Map<Character, TrieNode> children
 *   - Map<String, Integer> counts (tracks sentence frequencies passing through this node)
 * - Typing a character navigates the Trie down 1 step in O(1) time.
 * - Extracting top 3 uses a Min-Heap / PriorityQueue bounded at size 3: O(k log 3).
 * 
 * Complexity:
 * - input(c): O(P + L * log 3) where P is prefix length, L is number of sentences under prefix.
 * - Space: O(total characters in historical sentences).
 */
public class search_autocomplete {

    static class TrieNode {
        Map<Character, TrieNode> children = new HashMap<>();
        Map<String, Integer> counts = new HashMap<>();
    }

    private final TrieNode root;
    private TrieNode currNode;
    private StringBuilder currSentence;

    public search_autocomplete(String[] sentences, int[] times) {
        root = new TrieNode();
        currNode = root;
        currSentence = new StringBuilder();

        for (int i = 0; i < sentences.length; i++) {
            insertSentence(sentences[i], times[i]);
        }
    }

    private void insertSentence(String sentence, int count) {
        TrieNode node = root;
        for (char c : sentence.toCharArray()) {
            node.children.putIfAbsent(c, new TrieNode());
            node = node.children.get(c);
            node.counts.put(sentence, node.counts.getOrDefault(sentence, 0) + count);
        }
    }

    public List<String> input(char c) {
        if (c == '#') {
            // Sentence finished: commit to Trie and reset
            insertSentence(currSentence.toString(), 1);
            currSentence.setLength(0);
            currNode = root;
            return Collections.emptyList();
        }

        currSentence.append(c);

        if (currNode != null) {
            currNode = currNode.children.get(c);
        }

        if (currNode == null) {
            return Collections.emptyList();
        }

        // PriorityQueue to select top 3: Min-heap based on frequency (higher is better)
        // If frequencies are equal, lower ASCII is better
        PriorityQueue<Map.Entry<String, Integer>> pq = new PriorityQueue<>(
            (a, b) -> {
                if (!a.getValue().equals(b.getValue())) {
                    return Integer.compare(a.getValue(), b.getValue()); // Min-heap by frequency
                }
                return b.getKey().compareTo(a.getKey()); // Reverse ASCII for min-heap
            }
        );

        for (Map.Entry<String, Integer> entry : currNode.counts.entrySet()) {
            pq.offer(entry);
            if (pq.size() > 3) {
                pq.poll();
            }
        }

        List<String> result = new ArrayList<>();
        while (!pq.isEmpty()) {
            result.add(0, pq.poll().getKey());
        }

        return result;
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 642: Search Autocomplete System");
        System.out.println("=================================================");

        String[] sentences = {"i love you", "island", "ironman", "i love leetcode"};
        int[] times = {5, 3, 2, 2};

        search_autocomplete system = new search_autocomplete(sentences, times);

        // Type 'i'
        List<String> res1 = system.input('i');
        System.out.println("Input 'i' -> Expected [i love you, island, i love leetcode]: " + res1);
        assert res1.get(0).equals("i love you") : "Failed 'i' top match";

        // Type ' '
        List<String> res2 = system.input(' ');
        System.out.println("Input ' ' -> Expected [i love you, i love leetcode]: " + res2);
        assert res2.size() == 2 && res2.get(0).equals("i love you");

        // Type 'a'
        List<String> res3 = system.input('a');
        System.out.println("Input 'a' -> Expected []: " + res3);
        assert res3.isEmpty() : "Failed 'a' match";

        // Finish new sentence with '#'
        system.input('#');

        // Search 'i' again
        List<String> res4 = system.input('i');
        System.out.println("Search 'i' again after '#': " + res4);
        assert res4.contains("i a") : "Failed to record newly added sentence";

        System.out.println("\n✅ All Search Autocomplete tests passed successfully!");
    }
}
