import java.util.concurrent.atomic.*;

/**
 * Day 24: Concurrency — Volatile & Atomic Compare-And-Swap (CAS)
 * Demonstrates lock-free atomic counters using CPU CAS primitives.
 */
public class AtomicCounterCAS {

    private final AtomicInteger counter = new AtomicInteger(0);

    public int increment() {
        return counter.incrementAndGet();
    }

    public boolean compareAndSet(int expected, int update) {
        return counter.compareAndSet(expected, update);
    }

    public int get() { return counter.get(); }

    public static void main(String[] args) {
        AtomicCounterCAS c = new AtomicCounterCAS();
        assert c.increment() == 1;
        assert c.increment() == 2;
        assert c.compareAndSet(2, 100);
        assert !c.compareAndSet(2, 200) : "Expected CAS failure because value is now 100";
        assert c.get() == 100;
        System.out.println("Day 24 DSA AtomicCounterCAS verification passed!");
    }
}
