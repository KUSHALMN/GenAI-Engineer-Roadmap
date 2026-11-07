import java.util.concurrent.locks.*;

/**
 * Day 22: Concurrency — ReentrantReadWriteLock
 * Allows concurrent readers while guaranteeing mutual exclusion for writers.
 */
public class ReadWriteLockState {

    private final ReadWriteLock rwLock = new ReentrantReadWriteLock();
    private final Lock readLock = rwLock.readLock();
    private final Lock writeLock = rwLock.writeLock();
    private String modelCheckpoint = "v1.0.0";

    public String readCheckpoint() {
        readLock.lock();
        try { return modelCheckpoint; }
        finally { readLock.unlock(); }
    }

    public void updateCheckpoint(String newVersion) {
        writeLock.lock();
        try { this.modelCheckpoint = newVersion; }
        finally { writeLock.unlock(); }
    }

    public static void main(String[] args) {
        ReadWriteLockState state = new ReadWriteLockState();
        assert state.readCheckpoint().equals("v1.0.0");
        state.updateCheckpoint("v1.1.0");
        assert state.readCheckpoint().equals("v1.1.0");
        System.out.println("Day 22 DSA ReadWriteLockState verification passed!");
    }
}
