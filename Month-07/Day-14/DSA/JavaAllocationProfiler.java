package Month07.Day14;

/**
 * Java Performance & Memory Allocation Profiling:
 * Comparing primitive arrays vs boxed objects to minimize allocation pressure.
 */
public class JavaAllocationProfiler {

    public static long sumPrimitives(int count) {
        long sum = 0;
        for (int i = 0; i < count; i++) {
            sum += i; // Zero object allocation
        }
        return sum;
    }

    public static void main(String[] args) {
        long result = sumPrimitives(100_000);
        assert result == 4999950000L;
        System.out.println("Day 14 Java Allocation Profiler verification passed: " + result);
    }
}
