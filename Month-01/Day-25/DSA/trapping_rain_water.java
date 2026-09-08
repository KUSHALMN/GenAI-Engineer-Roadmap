import java.util.*;

/**
 * Problem: Trapping Rain Water (LeetCode 42 - Hard / Top FAANG Interview Question)
 * 
 * Given n non-negative integers representing an elevation map where the width
 * of each bar is 1, compute how much water it can trap after raining.
 * 
 * Approaches:
 * 1. Two Pointers (Optimal):
 *    - Maintain left and right pointers, and track maxLeft and maxRight.
 *    - Water trapped at current bar is determined by min(maxLeft, maxRight) - height[curr].
 *    - If maxLeft < maxRight: water depends on maxLeft, advance left++.
 *    - Else: water depends on maxRight, advance right--.
 *    - Time Complexity: O(n)
 *    - Space Complexity: O(1)
 * 
 * 2. Monotonic Decreasing Stack:
 *    - Maintain a stack of indices with decreasing heights.
 *    - When encountering height[i] > height[stack.peek()], we found a bounded trough.
 *    - Pop the bottom of the trough, compute distance and bounded height min(height[left], height[right]) - height[mid].
 *    - Time Complexity: O(n)
 *    - Space Complexity: O(n)
 */
public class trapping_rain_water {

    // ==========================================
    // Approach 1: Two Pointers (O(1) Auxiliary Space)
    // ==========================================
    public static int trapTwoPointers(int[] height) {
        if (height == null || height.length < 3) {
            return 0;
        }

        int left = 0;
        int right = height.length - 1;
        int maxLeft = 0;
        int maxRight = 0;
        int totalWater = 0;

        while (left < right) {
            if (height[left] <= height[right]) {
                if (height[left] >= maxLeft) {
                    maxLeft = height[left];
                } else {
                    totalWater += maxLeft - height[left];
                }
                left++;
            } else {
                if (height[right] >= maxRight) {
                    maxRight = height[right];
                } else {
                    totalWater += maxRight - height[right];
                }
                right--;
            }
        }

        return totalWater;
    }

    // ==========================================
    // Approach 2: Monotonic Decreasing Stack
    // ==========================================
    public static int trapStack(int[] height) {
        if (height == null || height.length < 3) {
            return 0;
        }

        Deque<Integer> stack = new ArrayDeque<>();
        int totalWater = 0;

        for (int i = 0; i < height.length; i++) {
            while (!stack.isEmpty() && height[i] > height[stack.peek()]) {
                int bottomIdx = stack.pop();
                if (stack.isEmpty()) {
                    break; // No left boundary to trap water
                }
                int leftIdx = stack.peek();
                int boundedHeight = Math.min(height[leftIdx], height[i]) - height[bottomIdx];
                int distance = i - leftIdx - 1;
                totalWater += boundedHeight * distance;
            }
            stack.push(i);
        }

        return totalWater;
    }

    // ==========================================
    // Test Harness & Verification
    // ==========================================
    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("🚀 Testing LeetCode 42: Trapping Rain Water (Java)");
        System.out.println("=================================================");

        // Test 1: Standard elevation map
        int[] h1 = {0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
        int res1TP = trapTwoPointers(h1);
        int res1Stack = trapStack(h1);
        System.out.println("Test 1 [0,1,0,2,1,0,1,3,2,1,2,1] -> Expected 6: TwoPointers=" + res1TP + ", Stack=" + res1Stack);
        assert res1TP == 6 && res1Stack == 6 : "Failed Test 1";

        // Test 2: Bowl shape
        int[] h2 = {4, 2, 0, 3, 2, 5};
        int res2TP = trapTwoPointers(h2);
        int res2Stack = trapStack(h2);
        System.out.println("Test 2 [4,2,0,3,2,5] -> Expected 9: TwoPointers=" + res2TP + ", Stack=" + res2Stack);
        assert res2TP == 9 && res2Stack == 9 : "Failed Test 2";

        // Test 3: Strictly ascending / descending (no water trapped)
        int[] h3 = {5, 4, 3, 2, 1};
        int res3 = trapTwoPointers(h3);
        System.out.println("Test 3 [5,4,3,2,1] -> Expected 0: " + res3);
        assert res3 == 0 : "Failed Test 3";

        // Test 4: Flat elevation
        int[] h4 = {3, 3, 3, 3};
        int res4 = trapTwoPointers(h4);
        System.out.println("Test 4 [3,3,3,3] -> Expected 0: " + res4);
        assert res4 == 0 : "Failed Test 4";

        System.out.println("\n✅ All Trapping Rain Water tests passed successfully!");
    }
}
