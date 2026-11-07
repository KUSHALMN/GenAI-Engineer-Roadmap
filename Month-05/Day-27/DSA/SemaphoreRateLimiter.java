import java.util.concurrent.*;

/**
 * Day 27: Concurrency — Semaphore for Concurrency Limiting
 * Restricts concurrent execution to a fixed number of permits.
 */
public class SemaphoreRateLimiter {

    private final Semaphore semaphore;

    public SemaphoreRateLimiter(int maxConcurrentRequests) {
        this.semaphore = new Semaphore(maxConcurrentRequests);
    }

    public boolean tryAcquireSlot() {
        return semaphore.tryAcquire();
    }

    public void releaseSlot() {
        semaphore.release();
    }

    public static void main(String[] args) {
        SemaphoreRateLimiter limiter = new SemaphoreRateLimiter(2);
        assert limiter.tryAcquireSlot();
        assert limiter.tryAcquireSlot();
        assert !limiter.tryAcquireSlot() : "Third acquire must fail (max 2 permits)";
        limiter.releaseSlot();
        assert limiter.tryAcquireSlot() : "Slot must now be available";
        System.out.println("Day 27 DSA SemaphoreRateLimiter verification passed!");
    }
}
