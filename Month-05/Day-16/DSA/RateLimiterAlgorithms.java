import java.util.*;

/**
 * Day 16: System Design / DSA — Rate Limiter Algorithms
 * Implements Token Bucket algorithm allowing bursting up to capacity with steady refill.
 *
 * Time Complexity: O(1) for allowRequest
 * Space Complexity: O(1)
 */
public class RateLimiterAlgorithms {

    static class TokenBucket {
        private final long capacity;
        private final double refillRatePerSecond;
        private double tokens;
        private long lastRefillTimestamp;

        public TokenBucket(long capacity, double refillRatePerSecond) {
            this.capacity = capacity;
            this.refillRatePerSecond = refillRatePerSecond;
            this.tokens = capacity;
            this.lastRefillTimestamp = System.currentTimeMillis();
        }

        public synchronized boolean allowRequest(int tokensRequested) {
            refill();
            if (tokens >= tokensRequested) {
                tokens -= tokensRequested;
                return true;
            }
            return false;
        }

        private void refill() {
            long now = System.currentTimeMillis();
            double secondsElapsed = (now - lastRefillTimestamp) / 1000.0;
            tokens = Math.min(capacity, tokens + (secondsElapsed * refillRatePerSecond));
            lastRefillTimestamp = now;
        }
    }

    public static void main(String[] args) {
        TokenBucket bucket = new TokenBucket(3, 1.0); // Capacity 3, 1 token per sec
        assert bucket.allowRequest(1);
        assert bucket.allowRequest(1);
        assert bucket.allowRequest(1);
        assert !bucket.allowRequest(1) : "Bucket should now be empty";
        System.out.println("Day 16 DSA RateLimiterAlgorithms verification passed!");
    }
}
