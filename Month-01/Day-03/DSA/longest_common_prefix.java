public class longest_common_prefix {
    // LeetCode #14 - Longest Common Prefix
    // Approach: Horizontal Scanning O(n*m)
    public String longestCommonPrefix(String[] strs) {
        if (strs == null || strs.length == 0) return "";
        String prefix = strs[0];

        for (int i = 1; i < strs.length; i++) {
            while (!strs[i].startsWith(prefix))
                prefix = prefix.substring(0, prefix.length() - 1);
            if (prefix.isEmpty()) return "";
        }
        return prefix;
    }

    public static void main(String[] args) {
        longest_common_prefix sol = new longest_common_prefix();
        System.out.println(sol.longestCommonPrefix(new String[]{"flower", "flow", "flight"})); // "fl"
        System.out.println(sol.longestCommonPrefix(new String[]{"dog", "racecar", "car"}));    // ""
    }
}
