import java.util.*;
import java.util.concurrent.*;

/**
 * Day 25: Advanced Design — Thread-Safe Cache with TTL (Time-To-Live)
 * Implements concurrent key-value storage with automatic expiration checking.
 */
public class ThreadSafeTTLCache<K, V> {

    static class CacheItem<V> {
        final V value;
        final long expiryTime;
        CacheItem(V value, long ttlMillis) {
            this.value = value;
            this.expiryTime = System.currentTimeMillis() + ttlMillis;
        }
        boolean isExpired() { return System.currentTimeMillis() > expiryTime; }
    }

    private final ConcurrentMap<K, CacheItem<V>> store = new ConcurrentHashMap<>();

    public void put(K key, V value, long ttlMillis) {
        store.put(key, new CacheItem<>(value, ttlMillis));
    }

    public V get(K key) {
        CacheItem<V> item = store.get(key);
        if (item == null) return null;
        if (item.isExpired()) {
            store.remove(key, item); // Atomic removal of expired entry
            return null;
        }
        return item.value;
    }

    public static void main(String[] args) throws InterruptedException {
        ThreadSafeTTLCache<String, String> cache = new ThreadSafeTTLCache<>();
        cache.put("k1", "v1", 50); // 50ms TTL
        assert cache.get("k1").equals("v1");

        Thread.sleep(60);
        assert cache.get("k1") == null : "Item should have expired";
        System.out.println("Day 25 DSA ThreadSafeTTLCache verification passed!");
    }
}
