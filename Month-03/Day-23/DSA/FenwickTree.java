package DSA;

/**
 * Fenwick Tree (Binary Indexed Tree - BIT)
 * Solves:
 * - Prefix sum queries in O(log N)
 * - Point updates in O(log N)
 * - Range Sum Query: sumRange(L, R) = query(R) - query(L - 1)
 * 
 * Bitwise Trick:
 * - isolates lowest set bit: i & (-i)
 * - parent in query tree: i -= (i & -i)
 * - parent in update tree: i += (i & -i)
 * 
 * Space Complexity: O(N)
 */
public class FenwickTree {
    private final int[] tree;
    private final int[] nums;
    private final int n;

    public FenwickTree(int[] nums) {
        this.n = nums.length;
        this.nums = new int[n];
        this.tree = new int[n + 1];

        for (int i = 0; i < n; i++) {
            update(i, nums[i]);
        }
    }

    /**
     * Point update: sets index to val
     */
    public void update(int index, int val) {
        int diff = val - nums[index];
        nums[index] = val;
        add(index + 1, diff);
    }

    private void add(int i, int delta) {
        while (i <= n) {
            tree[i] += delta;
            i += (i & (-i)); // Add lowest set bit
        }
    }

    /**
     * Computes prefix sum nums[0...i-1]
     */
    private int query(int i) {
        int sum = 0;
        while (i > 0) {
            sum += tree[i];
            i -= (i & (-i)); // Subtract lowest set bit
        }
        return sum;
    }

    /**
     * Range sum query nums[left...right] inclusive
     */
    public int sumRange(int left, int right) {
        return query(right + 1) - query(left);
    }

    public static void main(String[] args) {
        int[] arr = {1, 3, 5, 7, 9, 11};
        FenwickTree bit = new FenwickTree(arr);

        // Sum range [1, 3] -> arr[1] + arr[2] + arr[3] = 3 + 5 + 7 = 15
        System.out.println("Sum range [1, 3]: " + bit.sumRange(1, 3) + " (Expected: 15)");

        // Update index 1 to 10: arr becomes {1, 10, 5, 7, 9, 11}
        bit.update(1, 10);
        // New sum range [1, 3] -> 10 + 5 + 7 = 22
        System.out.println("Sum range [1, 3] after update: " + bit.sumRange(1, 3) + " (Expected: 22)");

        System.out.println("FenwickTree tests passed!");
    }
}
