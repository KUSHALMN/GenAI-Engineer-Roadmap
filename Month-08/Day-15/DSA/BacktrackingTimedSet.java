package Month08.Day15;

import java.util.ArrayList;
import java.util.List;

/**
 * Timed Set: Backtracking
 * LC 78: Subsets - O(2^N) time using recursive include/exclude backtracking.
 */
public class BacktrackingTimedSet {

    public static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(0, nums, new ArrayList<>(), result);
        return result;
    }

    private static void backtrack(int start, int[] nums, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current));
        for (int i = start; i < nums.length; i++) {
            current.add(nums[i]);
            backtrack(i + 1, nums, current, result);
            current.remove(current.size() - 1); // Undo decision
        }
    }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3};
        List<List<Integer>> subs = subsets(nums);
        assert subs.size() == 8; // 2^3 = 8 subsets

        System.out.println("Day 15 Backtracking Timed Set verification passed.");
    }
}
