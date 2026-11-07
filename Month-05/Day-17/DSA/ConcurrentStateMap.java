import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Day 17: Concurrency — ConcurrentHashMap & Atomic Data Structures
 * Demonstrates lock striping in ConcurrentHashMap and lock-free CAS operations with AtomicLong.
 */
public class ConcurrentStateMap {

    public static void main(String[] args) throws InterruptedException {
        ConcurrentMap<String, AtomicLong> metrics = new ConcurrentHashMap<>();
        int threads = 4;
        int incrementsPerThread = 10000;
        ExecutorService pool = Executors.newFixedThreadPool(threads);

        for (int i = 0; i < threads; i++) {
            pool.submit(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    metrics.computeIfAbsent("served_tokens", k -> new AtomicLong(0)).incrementAndGet();
                }
            });
        }

        pool.shutdown();
        pool.awaitTermination(2, TimeUnit.SECONDS);

        long totalTokens = metrics.get("served_tokens").get();
        System.out.println("Total atomic tokens counted: " + totalTokens);
        assert totalTokens == (long) threads * incrementsPerThread : "Must equal 40,000";
        System.out.println("Day 17 DSA ConcurrentStateMap verification passed!");
    }
}
