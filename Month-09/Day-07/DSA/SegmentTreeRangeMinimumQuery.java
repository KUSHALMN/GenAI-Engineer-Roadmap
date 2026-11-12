package Month_09.Day_07.DSA;

/**
 * Day 07: Timed DSA Problem Set — Segment Tree for Range Minimum Query (RMQ).
 * Focus: Segment Tree Construction in O(N), Point Update in O(log N), Range Query in O(log N).
 */
public class SegmentTreeRangeMinimumQuery {

    public static class SegmentTree {
        private final int[] tree;
        private final int n;

        public SegmentTree(int[] arr) {
            this.n = arr.length;
            this.tree = new int[4 * n];
            if (n > 0) {
                build(arr, 0, 0, n - 1);
            }
        }

        private void build(int[] arr, int node, int start, int end) {
            if (start == end) {
                tree[node] = arr[start];
                return;
            }
            int mid = (start + end) / 2;
            int leftChild = 2 * node + 1;
            int rightChild = 2 * node + 2;

            build(arr, leftChild, start, mid);
            build(arr, rightChild, mid + 1, end);
            tree[node] = Math.min(tree[leftChild], tree[rightChild]);
        }

        public void update(int idx, int val) {
            updateHelper(0, 0, n - 1, idx, val);
        }

        private void updateHelper(int node, int start, int end, int idx, int val) {
            if (start == end) {
                tree[node] = val;
                return;
            }
            int mid = (start + end) / 2;
            int leftChild = 2 * node + 1;
            int rightChild = 2 * node + 2;

            if (idx <= mid) {
                updateHelper(leftChild, start, mid, idx, val);
            } else {
                updateHelper(rightChild, mid + 1, end, idx, val);
            }
            tree[node] = Math.min(tree[leftChild], tree[rightChild]);
        }

        public int query(int l, int r) {
            return queryHelper(0, 0, n - 1, l, r);
        }

        private int queryHelper(int node, int start, int end, int l, int r) {
            if (r < start || end < l) {
                return Integer.MAX_VALUE; // Out of range
            }
            if (l <= start && end <= r) {
                return tree[node]; // Completely inside range
            }
            int mid = (start + end) / 2;
            int p1 = queryHelper(2 * node + 1, start, mid, l, r);
            int p2 = queryHelper(2 * node + 2, mid + 1, end, l, r);
            return Math.min(p1, p2);
        }
    }

    public static void main(String[] args) {
        int[] arr = {5, 2, 8, 3, 1, 9, 4};
        SegmentTree st = new SegmentTree(arr);

        assert st.query(0, 6) == 1 : "RMQ 0..6 failed";
        assert st.query(0, 3) == 2 : "RMQ 0..3 failed";
        assert st.query(2, 3) == 3 : "RMQ 2..3 failed";

        st.update(4, 10); // change value 1 at index 4 to 10
        assert st.query(0, 6) == 2 : "RMQ post-update failed: expected 2";
        assert st.query(4, 6) == 4 : "RMQ post-update failed: expected 4";

        System.out.println("Day 07 Segment Tree RMQ verification passed.");
    }
}
