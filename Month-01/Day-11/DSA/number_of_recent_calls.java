import java.util.LinkedList;
import java.util.Queue;

public class number_of_recent_calls {
    // LeetCode #933 - Number of Recent Calls
    // Approach: Queue O(1) amortized
    private Queue<Integer> queue = new LinkedList<>();

    public int ping(int t) {
        queue.offer(t);
        while (queue.peek() < t - 3000)
            queue.poll();
        return queue.size();
    }

    public static void main(String[] args) {
        number_of_recent_calls rc = new number_of_recent_calls();
        System.out.println(rc.ping(1));    // 1
        System.out.println(rc.ping(100));  // 2
        System.out.println(rc.ping(3001)); // 3
        System.out.println(rc.ping(3002)); // 3
    }
}
