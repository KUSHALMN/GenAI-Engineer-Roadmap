import java.util.*;

/**
 * Day 13: Dynamic Programming — Longest Increasing Subsequence (LIS)
 * Problem: Given an integer array nums, return the length of the longest strictly increasing subsequence.
 *
 * Algorithm 1: DP with O(n^2)
 * Algorithm 2: Patience Sorting with Binary Search O(n log n)
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 */
public class LongestIncreasingSubsequence {

    // O(n log n) solution using tails array and binary search
    public int lengthOfLIS(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int[] tails = new int[nums.length];
        int size = 0;

        for (int x : nums) {
            int i = 0, j = size;
            while (i < j) {
                int mid = (i + j) / 2;
                if (tails[mid] < x) {
                    i = mid + 1;
                } else {
                    j = mid;
                }
            }
            tails[i] = x;
            if (i == size) size++;
        }
        return size;
    }

    public static void main(String[] args) {
        LongestIncreasingSubsequence solver = new LongestIncreasingSubsequence();
        int[] nums = {10, 9, 2, 5, 3, 7, 101, 18};
        int lis = solver.lengthOfLIS(nums);

        System.out.println("LIS length for [10, 9, 2, 5, 3, 7, 101, 18]: " + lis);
        assert lis == 4 : "Expected 4 (e.g. [2, 3, 7, 101])";
        System.out.println("Day 13 DSA LongestIncreasingSubsequence verification passed!");
    }
}
