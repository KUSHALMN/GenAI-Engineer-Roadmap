package Month_09.Day_10.DSA;

import java.util.*;

/**
 * Day 10: Timed DSA Problem Set — Rabin-Karp Polynomial Rolling Hash.
 * Focus: LeetCode 187 (Repeated DNA Sequences) - O(N) Time, O(N) Space.
 */
public class RabinKarpRollingHash {

    public static List<String> findRepeatedDnaSequences(String s) {
        if (s == null || s.length() <= 10) return new ArrayList<>();

        int L = 10;
        int BASE = 4; // 4 nucleotides: A=0, C=1, G=2, T=3
        Map<Character, Integer> toInt = Map.of('A', 0, 'C', 1, 'G', 2, 'T', 3);

        int hash = 0;
        // Compute base^(L-1)
        int highestBase = 1;
        for (int i = 0; i < L - 1; i++) {
            highestBase *= BASE;
        }

        // Compute hash of first window of length L
        for (int i = 0; i < L; i++) {
            hash = hash * BASE + toInt.get(s.charAt(i));
        }

        Set<Integer> seenHashes = new HashSet<>();
        Set<String> output = new HashSet<>();
        seenHashes.add(hash);

        // Slide the window across string
        for (int start = 1; start <= s.length() - L; start++) {
            // Remove leftmost character
            hash -= toInt.get(s.charAt(start - 1)) * highestBase;
            // Shift left and add new incoming rightmost character
            hash = hash * BASE + toInt.get(s.charAt(start + L - 1));

            if (seenHashes.contains(hash)) {
                output.add(s.substring(start, start + L));
            } else {
                seenHashes.add(hash);
            }
        }
        return new ArrayList<>(output);
    }

    public static void main(String[] args) {
        String s1 = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT";
        List<String> res1 = findRepeatedDnaSequences(s1);
        assert res1.size() == 2 : "Test 1 failed count";
        assert res1.contains("AAAAACCCCC") && res1.contains("CCCCCAAAAA") : "Test 1 failed content";

        String s2 = "AAAAAAAAAAAAA";
        List<String> res2 = findRepeatedDnaSequences(s2);
        assert res2.size() == 1 && res2.contains("AAAAAAAAAA") : "Test 2 failed";

        System.out.println("Day 10 Rabin-Karp Rolling Hash verification passed.");
    }
}
