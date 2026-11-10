package Month07.Day12;

/**
 * Garbage Collection Concepts & Generational Allocation:
 * Models Young Generation (Eden -> Survivor) promotion to Tenured (Old) space.
 */
public class GarbageCollectionAnalyzer {

    public static class MemoryCollector {
        private int minorGcCount = 0;
        private int majorGcCount = 0;

        public void allocate(int ageThreshold, int objectAge) {
            if (objectAge >= ageThreshold) {
                majorGcCount++; // Promoted to Old Gen
            } else {
                minorGcCount++; // Collected in Young Gen
            }
        }

        public int getMinorGcCount() { return minorGcCount; }
        public int getMajorGcCount() { return majorGcCount; }
    }

    public static void main(String[] args) {
        MemoryCollector gc = new MemoryCollector();
        gc.allocate(15, 3);
        gc.allocate(15, 15); // Promoted
        assert gc.getMinorGcCount() == 1;
        assert gc.getMajorGcCount() == 1;

        System.out.println("Day 12 Garbage Collection Analyzer verification passed.");
    }
}
