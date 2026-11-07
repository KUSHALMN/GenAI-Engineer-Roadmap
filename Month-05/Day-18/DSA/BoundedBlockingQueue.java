import java.util.concurrent.locks.*;

/**
 * Day 18: Concurrency — Thread-Safe Bounded Blocking Queue
 * Implements enqueue and dequeue using ReentrantLock and Condition variables
 * (notFull and notEmpty).
 *
 * Time Complexity: O(1) for enqueue and dequeue
 * Space Complexity: O(capacity)
 */
public class BoundedBlockingQueue {

    private final int[] elements;
    private int head = 0, tail = 0, count = 0;
    private final Lock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    public BoundedBlockingQueue(int capacity) {
        this.elements = new int[capacity];
    }

    public void enqueue(int element) throws InterruptedException {
        lock.lock();
        try {
            while (count == elements.length) {
                notFull.await();
            }
            elements[tail] = element;
            tail = (tail + 1) % elements.length;
            count++;
            notEmpty.signal();
        } finally {
            lock.unlock();
        }
    }

    public int dequeue() throws InterruptedException {
        lock.lock();
        try {
            while (count == 0) {
                notEmpty.await();
            }
            int val = elements[head];
            head = (head + 1) % elements.length;
            count--;
            notFull.signal();
            return val;
        } finally {
            lock.unlock();
        }
    }

    public int size() {
        lock.lock();
        try { return count; }
        finally { lock.unlock(); }
    }

    public static void main(String[] args) throws InterruptedException {
        BoundedBlockingQueue q = new BoundedBlockingQueue(2);
        q.enqueue(10);
        q.enqueue(20);
        assert q.size() == 2;
        assert q.dequeue() == 10;
        assert q.dequeue() == 20;
        assert q.size() == 0;
        System.out.println("Day 18 DSA BoundedBlockingQueue verification passed!");
    }
}
