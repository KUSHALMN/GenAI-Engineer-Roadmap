import java.util.HashSet;

public class contains_duplicate {
    // LeetCode #217 - Contains Duplicate
    // Approach: HashSet O(n)
    public boolean containsDuplicate(int[] nums) {
        HashSet<Integer> set = new HashSet<>();
        for (int num : nums) {
            if (!set.add(num)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        contains_duplicate sol = new contains_duplicate();
        System.out.println(sol.containsDuplicate(new int[]{1, 2, 3, 1})); // true
        System.out.println(sol.containsDuplicate(new int[]{1, 2, 3, 4})); // false
    }
}
