import java.util.*;

/**
 * Day 14: Data Structure Design — Time-Based Key-Value Store
 * Stores keys at different timestamps and retrieves the key's value at timestamp_prev <= timestamp.
 *
 * Algorithm:
 * - HashMap<String, List<Entry>> where list is naturally sorted by timestamp.
 * - Binary search over timestamps to find largest timestamp <= target.
 *
 * Time Complexity: O(1) for set, O(log n) for get
 * Space Complexity: O(n)
 */
public class TimeMap {

    static class Data {
        int timestamp;
        String val;
        Data(int timestamp, String val) { this.timestamp = timestamp; this.val = val; }
    }

    private final Map<String, List<Data>> map = new HashMap<>();

    public void set(String key, String value, int timestamp) {
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(new Data(timestamp, value));
    }

    public String get(String key, int timestamp) {
        if (!map.containsKey(key)) return "";
        List<Data> list = map.get(key);

        int left = 0, right = list.size() - 1;
        String res = "";

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (list.get(mid).timestamp <= timestamp) {
                res = list.get(mid).val;
                left = mid + 1; // Try to find larger timestamp <= target
            } else {
                right = mid - 1;
            }
        }
        return res;
    }

    public static void main(String[] args) {
        TimeMap tm = new TimeMap();
        tm.set("foo", "bar", 1);
        assert tm.get("foo", 1).equals("bar");
        assert tm.get("foo", 3).equals("bar");
        tm.set("foo", "bar2", 4);
        assert tm.get("foo", 4).equals("bar2");
        assert tm.get("foo", 5).equals("bar2");
        assert tm.get("foo", 0).equals("");
        System.out.println("Day 14 DSA TimeMap verification passed!");
    }
}
