package Month07.Day31;

import java.util.concurrent.atomic.AtomicReference;

/**
 * Lock-Free Concurrency Mastery:
 * Michael-Scott Non-Blocking Queue using AtomicReference and CAS operations.
 */
public class ConcurrentNonBlockingQueue<T> {

    private static class Node<T> {
        final T value;
        final AtomicReference<Node<T>> next = new AtomicReference<>(null);
        Node(T val) { this.value = val; }
    }

    private final Node<T> dummy = new Node<>(null);
    private final AtomicReference<Node<T>> head = new AtomicReference<>(dummy);
    private final AtomicReference<Node<T>> tail = new AtomicReference<>(dummy);

    public void enqueue(T value) {
        Node<T> newNode = new Node<>(value);
        while (true) {
            Node<T> curTail = tail.get();
            Node<T> tailNext = curTail.next.get();
            if (curTail == tail.get()) {
                if (tailNext != null) {
                    tail.compareAndSet(curTail, tailNext); // Advance tail
                } else {
                    if (curTail.next.compareAndSet(null, newNode)) {
                        tail.compareAndSet(curTail, newNode);
                        return;
                    }
                }
            }
        }
    }

    public T dequeue() {
        while (true) {
            Node<T> curHead = head.get();
            Node<T> curTail = tail.get();
            Node<T> headNext = curHead.next.get();
            if (curHead == head.get()) {
                if (curHead == curTail) {
                    if (headNext == null) return null; // Queue empty
                    tail.compareAndSet(curTail, headNext);
                } else {
                    T val = headNext.value;
                    if (head.compareAndSet(curHead, headNext)) {
                        return val;
                    }
                }
            }
        }
    }

    public static void main(String[] args) {
        ConcurrentNonBlockingQueue<String> queue = new ConcurrentNonBlockingQueue<>();
        queue.enqueue("Task-1");
        queue.enqueue("Task-2");

        assert queue.dequeue().equals("Task-1");
        assert queue.dequeue().equals("Task-2");
        assert queue.dequeue() == null;

        System.out.println("Day 31 Concurrent Non-Blocking Queue verification passed.");
    }
}
