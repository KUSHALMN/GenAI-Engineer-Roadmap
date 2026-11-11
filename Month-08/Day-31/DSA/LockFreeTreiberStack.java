package Month_08.Day_31.DSA;

import java.util.concurrent.atomic.AtomicReference;

/**
 * Day 31: Advanced Concurrent DSA — Lock-Free Treiber Stack.
 * Non-blocking, thread-safe concurrent stack using AtomicReference and CAS (Compare-And-Swap).
 */
public class LockFreeTreiberStack<E> {

    private static class Node<E> {
        final E item;
        Node<E> next;
        Node(E item) { this.item = item; }
    }

    private final AtomicReference<Node<E>> top = new AtomicReference<>(null);

    public void push(E item) {
        Node<E> newHead = new Node<>(item);
        Node<E> oldHead;
        do {
            oldHead = top.get();
            newHead.next = oldHead;
        } while (!top.compareAndSet(oldHead, newHead));
    }

    public E pop() {
        Node<E> oldHead;
        Node<E> newHead;
        do {
            oldHead = top.get();
            if (oldHead == null) return null;
            newHead = oldHead.next;
        } while (!top.compareAndSet(oldHead, newHead));
        return oldHead.item;
    }

    public boolean isEmpty() {
        return top.get() == null;
    }

    public static void main(String[] args) {
        LockFreeTreiberStack<Integer> stack = new LockFreeTreiberStack<>();
        assert stack.isEmpty() : "Initial stack should be empty";

        stack.push(10);
        stack.push(20);
        stack.push(30);

        assert stack.pop() == 30 : "Pop 1 failed";
        assert stack.pop() == 20 : "Pop 2 failed";
        assert stack.pop() == 10 : "Pop 3 failed";
        assert stack.pop() == null : "Empty pop should return null";
        assert stack.isEmpty() : "Stack should now be empty";

        System.out.println("Day 31 Lock-Free Treiber Stack verification passed.");
    }
}
