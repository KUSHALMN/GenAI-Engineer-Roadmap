import java.util.HashMap;

public class ransom_note {
    // LeetCode #383 - Ransom Note
    // Approach: HashMap frequency count O(n)
    public boolean canConstruct(String ransomNote, String magazine) {
        HashMap<Character, Integer> map = new HashMap<>();
        for (char c : magazine.toCharArray())
            map.put(c, map.getOrDefault(c, 0) + 1);

        for (char c : ransomNote.toCharArray()) {
            if (map.getOrDefault(c, 0) == 0) return false;
            map.put(c, map.get(c) - 1);
        }
        return true;
    }

    public static void main(String[] args) {
        ransom_note sol = new ransom_note();
        System.out.println(sol.canConstruct("aa", "aab")); // true
        System.out.println(sol.canConstruct("aa", "ab"));  // false
    }
}
