package Month07.Day10;

import java.util.LinkedList;
import java.util.Queue;

/**
 * Producer-Consumer with Backpressure:
 * Thread-safe Bounded Blocking Queue using intrinsic monitors (wait / notifyAll).
 */
public class BoundedBlockingQueueProducerConsumer<T> {
    private final Queue<T> queue = new LinkedList<>();
    private final int capacity;

    public BoundedBlockingQueueProducerConsumer(int capacity) {
        this.capacity = capacity;
    }

    public synchronized void enqueue(T item) throws InterruptedException {
        while (queue.size() == capacity) {
            wait(); // Backpressure: wait until space is available
        }
        queue.add(item);
        notifyAll();
    }

    public synchronized T dequeue() throws InterruptedException {
        while (queue.isEmpty()) {
            wait(); // Wait until an item is produced
        }
        T item = queue.poll();
        notifyAll();
        return item;
    }

    public synchronized int size() {
        return queue.size();
    }

    public static void main(String[] args) throws InterruptedException {
        BoundedBlockingQueueProducerConsumer<Integer> q = new BoundedBlockingQueueProducerConsumer<>(2);
        q.enqueue(10);
        q.enqueue(20);
        assert q.size() == 2;

        int first = q.dequeue();
        assert first == 10;
        assert q.size() == 1;

        System.out.println("Day 10 Bounded Blocking Queue verification passed.");
    }
}
