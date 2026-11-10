package Month07.Day22;

/**
 * Low-Level Design (LLD): Resilient HTTP API Client
 * Circuit breaker states (CLOSED, OPEN, HALF_OPEN) and fallback handling.
 */
public class ResilientApiClientLowLevelDesign {

    public enum CircuitState { CLOSED, OPEN, HALF_OPEN }

    public static class ResilientClient {
        private CircuitState state = CircuitState.CLOSED;
        private int failureCount = 0;
        private final int failureThreshold = 3;

        public String executeCall(boolean simulateFailure) {
            if (state == CircuitState.OPEN) {
                return "FALLBACK_CACHED_RESPONSE";
            }
            if (simulateFailure) {
                failureCount++;
                if (failureCount >= failureThreshold) {
                    state = CircuitState.OPEN;
                }
                throw new RuntimeException("HTTP 500 Server Error");
            }
            failureCount = 0;
            return "SUCCESS_RESPONSE";
        }

        public CircuitState getState() { return state; }
    }

    public static void main(String[] args) {
        ResilientClient client = new ResilientClient();
        for (int i = 0; i < 3; i++) {
            try { client.executeCall(true); } catch (Exception ignored) {}
        }
        assert client.getState() == CircuitState.OPEN;
        assert client.executeCall(false).equals("FALLBACK_CACHED_RESPONSE");

        System.out.println("Day 22 Resilient API Client LLD verification passed.");
    }
}
