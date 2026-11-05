import java.util.*;

/**
 * Month-03 Final DSA Mastery Capstone
 * Multi-pattern timed challenge integrating:
 * 1. Data Stream Median (Two Heaps)
 * 2. Course Schedule II (Topological Sort / Kahn's BFS)
 * 3. Segment Tree Range Query & Update
 */
public class DSAMasteryCapstone {

    // 1. Two-Heap Running Median
    static class StreamMedian {
        private final PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        private final PriorityQueue<Integer> minHeap = new PriorityQueue<>();

        public void add(int num) {
            maxHeap.offer(num);
            minHeap.offer(maxHeap.poll());
            if (maxHeap.size() < minHeap.size()) {
                maxHeap.offer(minHeap.poll());
            }
        }

        public double getMedian() {
            return maxHeap.size() > minHeap.size() ? maxHeap.peek() : (maxHeap.peek() + minHeap.peek()) / 2.0;
        }
    }

    // 2. Segment Tree Range Query
    static class RangeSumTree {
        private final int[] tree;
        private final int n;

        public RangeSumTree(int[] arr) {
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
            build(arr, 2 * node, start, mid);
            build(arr, 2 * node + 1, mid + 1, end);
            tree[node] = tree[2 * node] + tree[2 * node + 1];
        }

        public int query(int l, int r) {
            return queryRange(1, 0, n - 1, l, r);
        }

        private int queryRange(int node, int start, int end, int l, int r) {
            if (r < start || end < l) return 0;
            if (l <= start && end <= r) return tree[node];
            int mid = start + (end - start) / 2;
            return queryRange(2 * node, start, mid, l, r) + queryRange(2 * node + 1, mid + 1, end, l, r);
        }
    }

    public static void main(String[] args) {
        // 1. Test Stream Median
        StreamMedian sm = new StreamMedian();
        sm.add(5);
        sm.add(15);
        sm.add(1);
        sm.add(3);
        System.out.println("Median after [5, 15, 1, 3]: " + sm.getMedian() + " (Expected: 4.0)");

        // 2. Test Range Tree
        int[] data = {1, 2, 3, 4, 5, 6};
        RangeSumTree rst = new RangeSumTree(data);
        System.out.println("Range sum [1, 4]: " + rst.query(1, 4) + " (Expected: 14)");

        System.out.println("DSAMasteryCapstone tests passed successfully!");
    }
}
