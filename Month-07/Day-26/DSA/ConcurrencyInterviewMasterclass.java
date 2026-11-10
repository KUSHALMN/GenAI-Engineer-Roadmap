package Month07.Day26;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Concurrency Masterclass:
 * Thread-safe Circular Ring Buffer using ReentrantLock and explicit Conditions.
 */
public class ConcurrencyInterviewMasterclass<T> {
    private final Object[] items;
    private int putIndex = 0, takeIndex = 0, count = 0;
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    public ConcurrencyInterviewMasterclass(int capacity) {
        items = new Object[capacity];
    }

    public void put(T x) throws InterruptedException {
        lock.lock();
        try {
            while (count == items.length) notFull.await();
            items[putIndex] = x;
            if (++putIndex == items.length) putIndex = 0;
            count++;
            notEmpty.signal();
        } finally {
            lock.unlock();
        }
    }

    @SuppressWarnings("unchecked")
    public T take() throws InterruptedException {
        lock.lock();
        try {
            while (count == 0) notEmpty.await();
            T x = (T) items[takeIndex];
            if (++takeIndex == items.length) takeIndex = 0;
            count--;
            notFull.signal();
            return x;
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        ConcurrencyInterviewMasterclass<String> ring = new ConcurrencyInterviewMasterclass<>(2);
        ring.put("A");
        ring.put("B");
        assert ring.take().equals("A");
        ring.put("C");
        assert ring.take().equals("B");

        System.out.println("Day 26 Concurrency Masterclass verification passed.");
    }
}
