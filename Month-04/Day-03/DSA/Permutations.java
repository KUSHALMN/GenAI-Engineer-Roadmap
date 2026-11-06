import java.util.*;

/**
 * Day 03: Backtracking — Permutations & Permutations II
 * Problem: Given an array nums of distinct integers, return all the possible permutations.
 *
 * Algorithm:
 * - Backtracking with a boolean `used[]` array or in-place swapping.
 * - At each step, iterate through all candidates and pick any element not currently used.
 *
 * Time Complexity: O(n * n!) where n is nums.length
 * Space Complexity: O(n) for recursion stack and used flag array.
 */
public class Permutations {

    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        boolean[] used = new boolean[nums.length];
        backtrack(nums, used, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(int[] nums, boolean[] used, List<Integer> current, List<List<Integer>> result) {
        if (current.size() == nums.length) {
            result.add(new ArrayList<>(current));
            return;
        }

        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;

            used[i] = true;
            current.add(nums[i]);
            backtrack(nums, used, current, result);
            current.remove(current.size() - 1);
            used[i] = false;
        }
    }

    public static void main(String[] args) {
        Permutations solver = new Permutations();
        int[] nums = {1, 2, 3};
        List<List<Integer>> perms = solver.permute(nums);

        System.out.println("Generated " + perms.size() + " permutations for [1, 2, 3]:");
        System.out.println(perms);

        assert perms.size() == 6 : "Expected 3! = 6 permutations";
        System.out.println("Day 03 DSA Permutations verification passed!");
    }
}
