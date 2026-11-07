import java.util.*;

/**
 * Day 15: System Design / DSA — Design Hit Counter
 * Tracks number of hits received in the past 5 minutes (300 seconds).
 *
 * Algorithm: Circular arrays of size 300 for timestamps and counts.
 * Time Complexity: O(1) for hit, O(300) = O(1) for getHits.
 * Space Complexity: O(1) fixed 300 elements.
 */
public class HitCounter {

    private final int[] times = new int[300];
    private final int[] hits = new int[300];

    public void hit(int timestamp) {
        int idx = timestamp % 300;
        if (times[idx] != timestamp) {
            times[idx] = timestamp;
            hits[idx] = 1;
        } else {
            hits[idx]++;
        }
    }

    public int getHits(int timestamp) {
        int total = 0;
        for (int i = 0; i < 300; i++) {
            if (timestamp - times[i] < 300) {
                total += hits[i];
            }
        }
        return total;
    }

    public static void main(String[] args) {
        HitCounter hc = new HitCounter();
        hc.hit(1);
        hc.hit(2);
        hc.hit(3);
        assert hc.getHits(4) == 3;
        hc.hit(300);
        assert hc.getHits(300) == 4;
        assert hc.getHits(301) == 3; // hit at timestamp 1 expired
        System.out.println("Day 15 DSA HitCounter verification passed!");
    }
}
