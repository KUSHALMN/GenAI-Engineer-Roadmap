"""
In-memory cache with Time-To-Live (TTL) expiration support.
Thread-safe with background and on-access cleanup.
"""

import threading
import time
from typing import Any, Dict, Optional, Tuple


class TTLCache:
    """
    Thread-safe In-Memory Cache with per-entry or default TTL.
    """

    def __init__(self, default_ttl_seconds: float = 300.0, max_size: int = 1000):
        self.default_ttl = default_ttl_seconds
        self.max_size = max_size
        self._store: Dict[str, Tuple[Any, float]] = {}  # key -> (value, expire_timestamp)
        self._lock = threading.RLock()

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        """Store key-value with specified TTL in seconds."""
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expire_at = time.time() + ttl

        with self._lock:
            # If at capacity and key is new, clean expired entries first
            if len(self._store) >= self.max_size and key not in self._store:
                self._cleanup_expired_locked()
                # If still at capacity, evict the oldest entry by expiration time
                if len(self._store) >= self.max_size:
                    oldest_key = min(self._store.keys(), key=lambda k: self._store[k][1])
                    del self._store[oldest_key]

            self._store[key] = (value, expire_at)

    def get(self, key: str) -> Optional[Any]:
        """Retrieve key value if present and unexpired."""
        with self._lock:
            if key not in self._store:
                return None
            value, expire_at = self._store[key]
            if time.time() > expire_at:
                # Expired - remove and return None
                del self._store[key]
                return None
            return value

    def delete(self, key: str) -> bool:
        """Remove key from cache."""
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def contains(self, key: str) -> bool:
        """Check if unexpired key exists."""
        return self.get(key) is not None

    def _cleanup_expired_locked(self) -> int:
        """Remove all expired entries. Must be called with lock held."""
        now = time.time()
        expired_keys = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired_keys:
            del self._store[k]
        return len(expired_keys)

    def cleanup_expired(self) -> int:
        """Public method to prune expired entries."""
        with self._lock:
            return self._cleanup_expired_locked()

    def size(self) -> int:
        """Return number of valid unexpired items."""
        with self._lock:
            self._cleanup_expired_locked()
            return len(self._store)

    def clear(self) -> None:
        """Empty the cache."""
        with self._lock:
            self._store.clear()


if __name__ == "__main__":
    cache = TTLCache(default_ttl_seconds=0.1, max_size=5)
    cache.set("model_response", "Generated text", ttl_seconds=0.2)
    assert cache.get("model_response") == "Generated text"
    time.sleep(0.25)
    assert cache.get("model_response") is None
    print("TTLCache tests passed successfully!")
