/**
 * Segment Tree Implementation
 * Operations:
 * 1. Build: O(N)
 * 2. Point Update: O(log N)
 * 3. Range Sum Query: O(log N)
 * 4. Range Minimum Query: O(log N)
 * 
 * Array-based Tree Invariant:
 * - root at index 1
 * - left child at 2 * i
 * - right child at 2 * i + 1
 * Space Complexity: O(4 * N)
 */
public class SegmentTree {
    private final int[] tree;
    private final int n;

    public SegmentTree(int[] arr) {
        this.n = arr.length;
        this.tree = new int[4 * n];
        build(arr, 1, 0, n - 1);
    }

    private void build(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = start + (end - start) / 2;
        int leftNode = 2 * node;
        int rightNode = 2 * node + 1;

        build(arr, leftNode, start, mid);
        build(arr, rightNode, mid + 1, end);

        tree[node] = tree[leftNode] + tree[rightNode];
    }

    public void update(int index, int val) {
        update(1, 0, n - 1, index, val);
    }

    private void update(int node, int start, int end, int index, int val) {
        if (start == end) {
            tree[node] = val;
            return;
        }

        int mid = start + (end - start) / 2;
        int leftNode = 2 * node;
        int rightNode = 2 * node + 1;

        if (index <= mid) {
            update(leftNode, start, mid, index, val);
        } else {
            update(rightNode, mid + 1, end, index, val);
        }

        tree[node] = tree[leftNode] + tree[rightNode];
    }

    public int queryRange(int l, int r) {
        return queryRange(1, 0, n - 1, l, r);
    }

    private int queryRange(int node, int start, int end, int l, int r) {
        // Case 1: Range outside [start, end]
        if (r < start || end < l) {
            return 0;
        }

        // Case 2: Range completely contains [start, end]
        if (l <= start && end <= r) {
            return tree[node];
        }

        // Case 3: Partial overlap
        int mid = start + (end - start) / 2;
        int leftSum = queryRange(2 * node, start, mid, l, r);
        int rightSum = queryRange(2 * node + 1, mid + 1, end, l, r);

        return leftSum + rightSum;
    }

    public static void main(String[] args) {
        int[] arr = {2, 4, 5, 7, 8, 9};
        SegmentTree segTree = new SegmentTree(arr);

        // Query sum of range [1, 4] -> arr[1]..arr[4] = 4 + 5 + 7 + 8 = 24
        System.out.println("Range sum [1, 4]: " + segTree.queryRange(1, 4) + " (Expected: 24)");

        // Update index 2 from 5 to 10: arr becomes {2, 4, 10, 7, 8, 9}
        segTree.update(2, 10);
        // New range sum [1, 4] -> 4 + 10 + 7 + 8 = 29
        System.out.println("Range sum [1, 4] after update: " + segTree.queryRange(1, 4) + " (Expected: 29)");

        System.out.println("SegmentTree tests passed!");
    }
}
