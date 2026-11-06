import java.util.*;

/**
 * Day 26: String Matching — Rabin-Karp Substring Search
 * Problem: Find all occurrences of pattern p in text t using rolling hash.
 *
 * Algorithm:
 * - Compute hash of pattern and first window of text using polynomial rolling hash.
 * - Roll hash in O(1) for subsequent windows: hash = (hash - leading_char * power) * base + trailing_char.
 * - Verify characters on hash match to prevent false positives from collisions.
 *
 * Time Complexity: Average O(N + M), Worst O(N * M)
 * Space Complexity: O(1) auxiliary.
 */
public class RabinKarpSubstringSearch {

    private static final int PRIME = 101;
    private static final int BASE = 256;

    public List<Integer> search(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        int n = text.length();
        int m = pattern.length();
        if (m > n || m == 0) return matches;

        long patternHash = 0;
        long windowHash = 0;
        long h = 1;

        // h = (BASE^(m-1)) % PRIME
        for (int i = 0; i < m - 1; i++) h = (h * BASE) % PRIME;

        for (int i = 0; i < m; i++) {
            patternHash = (BASE * patternHash + pattern.charAt(i)) % PRIME;
            windowHash = (BASE * windowHash + text.charAt(i)) % PRIME;
        }

        for (int i = 0; i <= n - m; i++) {
            if (patternHash == windowHash) {
                // Verify to avoid hash collisions
                if (text.substring(i, i + m).equals(pattern)) {
                    matches.add(i);
                }
            }
            if (i < n - m) {
                windowHash = (BASE * (windowHash - text.charAt(i) * h) + text.charAt(i + m)) % PRIME;
                if (windowHash < 0) windowHash += PRIME;
            }
        }
        return matches;
    }

    public static void main(String[] args) {
        RabinKarpSubstringSearch solver = new RabinKarpSubstringSearch();
        String text = "ABABDABACDABABCABAB";
        String pattern = "ABABCABAB";
        List<Integer> matches = solver.search(text, pattern);

        System.out.println("Pattern found at indices: " + matches);
        assert matches.contains(10);
        System.out.println("Day 26 DSA RabinKarpSubstringSearch verification passed!");
    }
}
