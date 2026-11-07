import java.util.concurrent.atomic.*;

/**
 * Day 31: Advanced Concurrency — Lock-Free High-Throughput Ring Buffer
 * Implements a lock-free single-producer single-consumer circular ring buffer.
 */
public class ConcurrentRingBuffer<T> {

    private final Object[] buffer;
    private final int capacity;
    private final AtomicLong writeSeq = new AtomicLong(0);
    private final AtomicLong readSeq = new AtomicLong(0);

    public ConcurrentRingBuffer(int capacity) {
        this.capacity = capacity;
        this.buffer = new Object[capacity];
    }

    public boolean offer(T item) {
        long currentWrite = writeSeq.get();
        long currentRead = readSeq.get();
        if (currentWrite - currentRead >= capacity) {
            return false; // Buffer full
        }
        buffer[(int) (currentWrite % capacity)] = item;
        writeSeq.lazySet(currentWrite + 1);
        return true;
    }

    @SuppressWarnings("unchecked")
    public T poll() {
        long currentRead = readSeq.get();
        long currentWrite = writeSeq.get();
        if (currentRead >= currentWrite) {
            return null; // Buffer empty
        }
        T item = (T) buffer[(int) (currentRead % capacity)];
        readSeq.lazySet(currentRead + 1);
        return item;
    }

    public static void main(String[] args) {
        ConcurrentRingBuffer<String> ring = new ConcurrentRingBuffer<>(2);
        assert ring.offer("Token-1");
        assert ring.offer("Token-2");
        assert !ring.offer("Token-3") : "Buffer full";
        assert ring.poll().equals("Token-1");
        assert ring.offer("Token-3");
        assert ring.poll().equals("Token-2");
        assert ring.poll().equals("Token-3");
        assert ring.poll() == null;
        System.out.println("Day 31 DSA ConcurrentRingBuffer verification passed!");
    }
}
