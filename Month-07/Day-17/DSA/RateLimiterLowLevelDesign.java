package Month07.Day17;

import java.util.LinkedList;
import java.util.Queue;

/**
 * Low-Level Design (LLD): Sliding Window Log Rate Limiter
 * Provides thread-safe, precise rate limiting by timestamp log retention.
 */
public class RateLimiterLowLevelDesign {

    public static class SlidingWindowLogRateLimiter {
        private final Queue<Long> requestTimestamps = new LinkedList<>();
        private final int maxRequests;
        private final long windowSizeMillis;

        public SlidingWindowLogRateLimiter(int maxRequests, long windowSizeMillis) {
            this.maxRequests = maxRequests;
            this.windowSizeMillis = windowSizeMillis;
        }

        public synchronized boolean allowRequest(long currentTimeMillis) {
            long boundary = currentTimeMillis - windowSizeMillis;
            while (!requestTimestamps.isEmpty() && requestTimestamps.peek() <= boundary) {
                requestTimestamps.poll();
            }
            if (requestTimestamps.size() < maxRequests) {
                requestTimestamps.add(currentTimeMillis);
                return true;
            }
            return false;
        }
    }

    public static void main(String[] args) {
        SlidingWindowLogRateLimiter limiter = new SlidingWindowLogRateLimiter(2, 1000);
        long now = System.currentTimeMillis();
        assert limiter.allowRequest(now);
        assert limiter.allowRequest(now + 10);
        assert !limiter.allowRequest(now + 20); // Third request blocked!

        // After window expires
        assert limiter.allowRequest(now + 1050);
        System.out.println("Day 17 Rate Limiter LLD verification passed.");
    }
}
