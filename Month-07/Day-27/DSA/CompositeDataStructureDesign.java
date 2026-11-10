package Month07.Day27;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

/**
 * Composite Data Structure Design:
 * O(1) Insert, O(1) Delete, and O(1) GetRandom using HashMap + ArrayList swap-with-last.
 */
public class CompositeDataStructureDesign {

    public static class RandomizedSet {
        private final List<Integer> nums = new ArrayList<>();
        private final Map<Integer, Integer> valToIndex = new HashMap<>();
        private final Random rand = new Random();

        public boolean insert(int val) {
            if (valToIndex.containsKey(val)) return false;
            valToIndex.put(val, nums.size());
            nums.add(val);
            return true;
        }

        public boolean remove(int val) {
            if (!valToIndex.containsKey(val)) return false;
            int idx = valToIndex.get(val);
            int lastVal = nums.get(nums.size() - 1);

            nums.set(idx, lastVal);
            valToIndex.put(lastVal, idx);

            nums.remove(nums.size() - 1);
            valToIndex.remove(val);
            return true;
        }

        public int getRandom() {
            return nums.get(rand.nextInt(nums.size()));
        }
    }

    public static void main(String[] args) {
        RandomizedSet set = new RandomizedSet();
        assert set.insert(10);
        assert set.insert(20);
        assert !set.insert(10);

        assert set.remove(10);
        assert !set.remove(10);
        assert set.getRandom() == 20;

        System.out.println("Day 27 Composite Data Structure verification passed.");
    }
}
