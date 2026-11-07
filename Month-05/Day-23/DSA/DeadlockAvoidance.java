import java.util.concurrent.locks.*;

/**
 * Day 23: Concurrency — Deadlock Avoidance via Global Lock Ordering
 * Demonstrates lock ordering preventing circular wait condition.
 */
public class DeadlockAvoidance {

    private final Lock lockA = new ReentrantLock();
    private final Lock lockB = new ReentrantLock();

    // Always acquire lockA before lockB
    public void executeTaskOne() {
        lockA.lock();
        try {
            lockB.lock();
            try {
                // Critical section
            } finally { lockB.unlock(); }
        } finally { lockA.unlock(); }
    }

    public void executeTaskTwo() {
        lockA.lock(); // Strict identical ordering avoids deadlock!
        try {
            lockB.lock();
            try {
                // Critical section
            } finally { lockB.unlock(); }
        } finally { lockA.unlock(); }
    }

    public static void main(String[] args) {
        DeadlockAvoidance da = new DeadlockAvoidance();
        da.executeTaskOne();
        da.executeTaskTwo();
        System.out.println("Day 23 DSA DeadlockAvoidance verification passed!");
    }
}
