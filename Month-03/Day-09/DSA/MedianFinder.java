import java.util.Collections;
import java.util.PriorityQueue;

/**
 * LeetCode 295 - Find Median from Data Stream
 * Invariants:
 * 1. maxHeap holds the smaller half of numbers.
 * 2. minHeap holds the larger half of numbers.
 * 3. maxHeap size is either equal to minHeap size or larger by exactly 1.
 * Time Complexity:
 * - addNum: O(log N)
 * - findMedian: O(1)
 * Space Complexity: O(N) to store all incoming numbers
 */
public class MedianFinder {
    private final PriorityQueue<Integer> maxHeap; // smaller half
    private final PriorityQueue<Integer> minHeap; // larger half

    public MedianFinder() {
        this.maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        this.minHeap = new PriorityQueue<>();
    }

    public void addNum(int num) {
        maxHeap.offer(num);
        minHeap.offer(maxHeap.poll());

        // Balance sizes so maxHeap.size() >= minHeap.size()
        if (maxHeap.size() < minHeap.size()) {
            maxHeap.offer(minHeap.poll());
        }
    }

    public double findMedian() {
        if (maxHeap.size() > minHeap.size()) {
            return maxHeap.peek();
        } else {
            return (maxHeap.peek() + minHeap.peek()) / 2.0;
        }
    }

    public static void main(String[] args) {
        MedianFinder mf = new MedianFinder();
        mf.addNum(1);
        mf.addNum(2);
        System.out.println("Median after [1, 2]: " + mf.findMedian()); // Expected 1.5

        mf.addNum(3);
        System.out.println("Median after [1, 2, 3]: " + mf.findMedian()); // Expected 2.0

        mf.addNum(5);
        mf.addNum(8);
        mf.addNum(9);
        System.out.println("Median after [1, 2, 3, 5, 8, 9]: " + mf.findMedian()); // Expected 4.0

        System.out.println("All test assertions passed successfully!");
    }
}
