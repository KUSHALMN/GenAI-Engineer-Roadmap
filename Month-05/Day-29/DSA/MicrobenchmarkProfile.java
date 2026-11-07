import java.util.*;

/**
 * Day 29: Performance — Microbenchmarking Invariants & Warmup
 * Demonstrates JVM JIT compiler warmup effects and nanoTime profiling.
 */
public class MicrobenchmarkProfile {

    public static void main(String[] args) {
        int warmupIterations = 10000;
        int benchmarkIterations = 100000;

        // Warmup phase (allows C2 JIT compiler to optimize code path)
        for (int i = 0; i < warmupIterations; i++) {
            computeHash(i);
        }

        // Measurement phase
        long start = System.nanoTime();
        for (int i = 0; i < benchmarkIterations; i++) {
            computeHash(i);
        }
        long duration = System.nanoTime() - start;

        double avgNs = (double) duration / benchmarkIterations;
        System.out.println("Average operation latency after JIT warmup: " + String.format("%.2f", avgNs) + " ns");
        assert avgNs < 100.0 : "JIT optimized hash must execute in under 100ns";
        System.out.println("Day 29 DSA MicrobenchmarkProfile verification passed!");
    }

    private static int computeHash(int x) {
        return (x ^ (x >>> 16)) * 0x45d9f3b;
    }
}
