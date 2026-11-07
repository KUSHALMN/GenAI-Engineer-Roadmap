import java.util.*;

/**
 * Day 13: Data Structure Design — Insert Delete GetRandom O(1)
 * Combines ArrayList (for O(1) random index access) and HashMap (for O(1) value-to-index lookup).
 * On deletion, swaps the target element with the last element of the list to remove in O(1).
 */
public class RandomizedSet {

    private final List<Integer> list = new ArrayList<>();
    private final Map<Integer, Integer> map = new HashMap<>(); // val -> index in list
    private final Random rand = new Random(42);

    public boolean insert(int val) {
        if (map.containsKey(val)) return false;
        map.put(val, list.size());
        list.add(val);
        return true;
    }

    public boolean remove(int val) {
        if (!map.containsKey(val)) return false;
        int idx = map.get(val);
        int lastVal = list.get(list.size() - 1);

        // Swap with last element
        list.set(idx, lastVal);
        map.put(lastVal, idx);

        // Remove last
        list.remove(list.size() - 1);
        map.remove(val);
        return true;
    }

    public int getRandom() {
        return list.get(rand.nextInt(list.size()));
    }

    public static void main(String[] args) {
        RandomizedSet rs = new RandomizedSet();
        assert rs.insert(1);
        assert !rs.remove(2);
        assert rs.insert(2);
        int r = rs.getRandom();
        assert r == 1 || r == 2;
        assert rs.remove(1);
        assert !rs.insert(2);
        assert rs.getRandom() == 2;
        System.out.println("Day 13 DSA RandomizedSet verification passed!");
    }
}
