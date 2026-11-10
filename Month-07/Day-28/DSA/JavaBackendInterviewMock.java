package Month07.Day28;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Senior Java Backend Mock:
 * Scalable Hit Counter & Throughput Tracker using thread-safe ConcurrentHashMap & AtomicLong.
 */
public class JavaBackendInterviewMock {

    public static class HighThroughputMetricsCounter {
        private final ConcurrentHashMap<String, AtomicLong> counters = new ConcurrentHashMap<>();

        public void increment(String metricKey) {
            counters.computeIfAbsent(metricKey, k -> new AtomicLong(0)).incrementAndGet();
        }

        public long getCount(String metricKey) {
            AtomicLong val = counters.get(metricKey);
            return val != null ? val.get() : 0L;
        }
    }

    public static void main(String[] args) {
        HighThroughputMetricsCounter metrics = new HighThroughputMetricsCounter();
        metrics.increment("api.requests.total");
        metrics.increment("api.requests.total");

        assert metrics.getCount("api.requests.total") == 2L;
        assert metrics.getCount("non.existent") == 0L;

        System.out.println("Day 28 Java Backend Interview Mock verification passed.");
    }
}
