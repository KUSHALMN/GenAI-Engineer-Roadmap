public class ComprehensiveMockInterview {
    // 1. LC 42: Trapping Rain Water
    public static int trap(int[] height) {
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0, water = 0;
        while (left < right) {
            if (height[left] <= height[right]) {
                if (height[left] >= leftMax) leftMax = height[left];
                else water += leftMax - height[left];
                left++;
            } else {
                if (height[right] >= rightMax) rightMax = height[right];
                else water += rightMax - height[right];
                right--;
            }
        }
        return water;
    }

    public static void main(String[] args) {
        System.out.println("=== FAANG Comprehensive Timed Mock ===");
        int[] h = {0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
        int trapped = trap(h);
        System.out.println("LC 42 Trapped Water: " + trapped + " (Expected 6)");
        assert trapped == 6 : "Mock failed";
        System.out.println("Timed mock interview passed!");
    }
}
