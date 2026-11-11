package Month_08.Day_20.DSA;

/**
 * Day 20: Timed DSA Problem Set — Fenwick Tree (Binary Indexed Tree) for Dynamic Range Queries.
 * Focus: LeetCode 307 (Range Sum Query - Mutable) - O(log N) Update, O(log N) Query.
 */
public class RangeQueryFenwickTree {

    public static class FenwickTree {
        private final int[] tree;
        private final int n;

        public FenwickTree(int n) {
            this.n = n;
            this.tree = new int[n + 1];
        }

        public void add(int i, int delta) {
            for (; i <= n; i += i & (-i)) {
                tree[i] += delta;
            }
        }

        public int query(int i) {
            int sum = 0;
            for (; i > 0; i -= i & (-i)) {
                sum += tree[i];
            }
            return sum;
        }

        public int rangeSum(int left, int right) {
            return query(right) - query(left - 1);
        }
    }

    public static class NumArray {
        private final FenwickTree bit;
        private final int[] nums;

        public NumArray(int[] nums) {
            this.nums = nums.clone();
            this.bit = new FenwickTree(nums.length);
            for (int i = 0; i < nums.length; i++) {
                bit.add(i + 1, nums[i]);
            }
        }

        public void update(int index, int val) {
            int delta = val - nums[index];
            nums[index] = val;
            bit.add(index + 1, delta);
        }

        public int sumRange(int left, int right) {
            return bit.rangeSum(left + 1, right + 1);
        }
    }

    public static void main(String[] args) {
        int[] nums = {1, 3, 5};
        NumArray numArray = new NumArray(nums);
        assert numArray.sumRange(0, 2) == 9 : "Test 1 Failed";
        numArray.update(1, 2); // nums becomes {1, 2, 5}
        assert numArray.sumRange(0, 2) == 8 : "Test 2 Failed";
        assert numArray.sumRange(1, 2) == 7 : "Test 3 Failed";

        System.out.println("Day 20 Range Query Fenwick Tree verification passed.");
    }
}
