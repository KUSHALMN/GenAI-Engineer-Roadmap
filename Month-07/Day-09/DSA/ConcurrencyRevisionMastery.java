package Month07.Day09;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Concurrency Revision Mastery:
 * Atomic CAS Counters, CountDownLatch synchronization barriers, and thread pools.
 */
public class ConcurrencyRevisionMastery {

    public static int runConcurrentTasks(int numThreads, int incrementsPerThread) throws InterruptedException {
        AtomicInteger counter = new AtomicInteger(0);
        CountDownLatch latch = new CountDownLatch(numThreads);
        ExecutorService pool = Executors.newFixedThreadPool(numThreads);

        for (int i = 0; i < numThreads; i++) {
            pool.submit(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.incrementAndGet();
                }
                latch.countDown();
            });
        }

        latch.await();
        pool.shutdown();
        return counter.get();
    }

    public static void main(String[] args) throws InterruptedException {
        int total = runConcurrentTasks(4, 2500);
        assert total == 10000;
        System.out.println("Day 09 Concurrency Revision verification passed: " + total);
    }
}
