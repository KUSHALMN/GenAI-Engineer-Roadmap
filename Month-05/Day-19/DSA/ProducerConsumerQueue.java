import java.util.concurrent.*;

/**
 * Day 19: Concurrency — Producer-Consumer Pattern
 * Implements concurrent batch production and consumption using ArrayBlockingQueue.
 */
public class ProducerConsumerQueue {

    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);
        int totalItems = 10;
        CountDownLatch latch = new CountDownLatch(totalItems);

        // Producer thread
        Thread producer = new Thread(() -> {
            try {
                for (int i = 1; i <= totalItems; i++) {
                    queue.put("Inference-Token-" + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        // Consumer thread
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 1; i <= totalItems; i++) {
                    String item = queue.take();
                    latch.countDown();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        producer.start();
        consumer.start();

        boolean completed = latch.await(2, TimeUnit.SECONDS);
        assert completed : "All tokens should be consumed";
        System.out.println("Day 19 DSA ProducerConsumerQueue verification passed!");
    }
}
