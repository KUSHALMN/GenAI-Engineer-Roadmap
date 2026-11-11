package Month_08.Day_22.DSA;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Day 22: Timed DSA Problem Set — Concurrency Control & Bounded Resource Throttling.
 * Implementing a thread-safe Semaphore-based Bounded Concurrency Limiter with timeouts.
 */
public class BoundedConcurrencyLimiter {

    private final Semaphore semaphore;
    private final int maxConcurrent;
    private final AtomicInteger activeExecutions = new AtomicInteger(0);

    public BoundedConcurrencyLimiter(int maxConcurrent) {
        this.maxConcurrent = maxConcurrent;
        this.semaphore = new Semaphore(maxConcurrent, true); // Fair semaphore
    }

    public <T> T execute(Callable<T> task, long timeoutMs) throws Exception {
        boolean acquired = semaphore.tryAcquire(timeoutMs, TimeUnit.MILLISECONDS);
        if (!acquired) {
            throw new TimeoutException("Rate limit / concurrency ceiling exceeded.");
        }
        try {
            activeExecutions.incrementAndGet();
            return task.call();
        } finally {
            activeExecutions.decrementAndGet();
            semaphore.release();
        }
    }

    public int getActiveCount() {
        return activeExecutions.get();
    }

    public static void main(String[] args) throws Exception {
        BoundedConcurrencyLimiter limiter = new BoundedConcurrencyLimiter(2);

        Callable<String> fastTask = () -> {
            Thread.sleep(50);
            return "SUCCESS";
        };

        // Submit 2 parallel tasks
        ExecutorService executor = Executors.newFixedThreadPool(4);
        Future<String> f1 = executor.submit(() -> limiter.execute(fastTask, 200));
        Future<String> f2 = executor.submit(() -> limiter.execute(fastTask, 200));

        assert f1.get().equals("SUCCESS") : "f1 failed";
        assert f2.get().equals("SUCCESS") : "f2 failed";

        executor.shutdown();
        System.out.println("Day 22 Bounded Concurrency Limiter verification passed.");
    }
}
