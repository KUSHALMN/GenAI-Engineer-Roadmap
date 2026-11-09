import java.util.*;

public class BacktrackingCombinations {
    // 1. LC 78: Subsets
    public static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrackSubsets(nums, 0, new ArrayList<>(), result);
        return result;
    }

    private static void backtrackSubsets(int[] nums, int start, List<Integer> curr, List<List<Integer>> result) {
        result.add(new ArrayList<>(curr));
        for (int i = start; i < nums.length; i++) {
            curr.add(nums[i]);
            backtrackSubsets(nums, i + 1, curr, result);
            curr.remove(curr.size() - 1);
        }
    }

    // 2. LC 39: Combination Sum
    public static List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(candidates);
        backtrackCombSum(candidates, target, 0, new ArrayList<>(), result);
        return result;
    }

    private static void backtrackCombSum(int[] cands, int remain, int start, List<Integer> curr, List<List<Integer>> result) {
        if (remain == 0) {
            result.add(new ArrayList<>(curr));
            return;
        }
        for (int i = start; i < cands.length; i++) {
            if (cands[i] > remain) break;
            curr.add(cands[i]);
            backtrackCombSum(cands, remain - cands[i], i, curr, result); // Reuse candidate
            curr.remove(curr.size() - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println("=== Backtracking Patterns Verification ===");
        int[] nums = {1, 2, 3};
        List<List<Integer>> subs = subsets(nums);
        System.out.println("LC 78 (Subsets of [1,2,3]): " + subs.size() + " subsets");
        assert subs.size() == 8 : "Expected 2^3 = 8 subsets";

        int[] cands = {2, 3, 6, 7};
        List<List<Integer>> combs = combinationSum(cands, 7);
        System.out.println("LC 39 (Combination Sum = 7): " + combs);
        assert combs.size() == 2 : "Expected 2 combinations [[2,2,3], [7]]";
        System.out.println("Backtracking tests passed!");
    }
}
