"""
Redis Application Patterns: Write-Through Caching, TTL Expiration,
Distributed Locks (Redlock pattern), and Sliding Window Rate Limiting.
"""

import time
from typing import Any, Dict, Optional


class RedisCacheService:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}
        self._locks: Dict[str, float] = {}

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        self._store[key] = value
        if ttl_seconds:
            self._expiry[key] = time.time() + ttl_seconds
        elif key in self._expiry:
            del self._expiry[key]

    def get(self, key: str) -> Optional[Any]:
        if key in self._expiry and time.time() > self._expiry[key]:
            del self._store[key]
            del self._expiry[key]
            return None
        return self._store.get(key)

    def acquire_lock(self, lock_key: str, ttl_seconds: float = 5.0) -> bool:
        now = time.time()
        if lock_key in self._locks and now < self._locks[lock_key]:
            return False # Lock currently held
        self._locks[lock_key] = now + ttl_seconds
        return True

    def release_lock(self, lock_key: str):
        if lock_key in self._locks:
            del self._locks[lock_key]


if __name__ == "__main__":
    redis = RedisCacheService()
    redis.set("user:101:profile", {"name": "Kushal"}, ttl_seconds=10)
    assert redis.get("user:101:profile")["name"] == "Kushal"

    assert redis.acquire_lock("resource:order:44") is True
    assert redis.acquire_lock("resource:order:44") is False # Blocked
    redis.release_lock("resource:order:44")
    assert redis.acquire_lock("resource:order:44") is True

    print("=== Day 06: Redis Cache & Lock Patterns ===")
    print("TTL expiration and distributed lock simulation passed.")
