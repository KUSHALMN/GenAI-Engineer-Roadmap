package Month08.Day02;

/**
 * Timed Set: Strings & Frequency Maps
 * LC 242: Valid Anagram - O(N) time and O(1) space using fixed array.
 */
public class StringsFrequencyMaps {

    public static boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        int[] counts = new int[26];
        for (int i = 0; i < s.length(); i++) {
            counts[s.charAt(i) - 'a']++;
            counts[t.charAt(i) - 'a']--;
        }
        for (int c : counts) {
            if (c != 0) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        assert isAnagram("anagram", "nagaram");
        assert !isAnagram("rat", "car");

        System.out.println("Day 02 Strings & Frequency Maps verification passed.");
    }
}
