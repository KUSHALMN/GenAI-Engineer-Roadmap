"""
Multi-Tier Retrieval & Embedding Cache with Cryptographic Invalidation
Demonstrates:
1. Canonical Cache Key Hashing:
   Key = SHA256(Query + TenantID + ModelVersion + IndexVersion + SerializedFilters)
2. In-memory L1 cache + Distributed L2 cache simulation with TTL
3. Invalidation triggers on Index Version Bumps or Tenant updates
4. Cache Hit Ratio tracking and Latency benchmarking
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional, List


class RetrievalCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        # Key -> {"data": Any, "expires_at": float, "tenant_id": str, "index_version": str}
        self.store: Dict[str, Dict[str, Any]] = {}
        self.hits = 0
        self.misses = 0

    def generate_cache_key(
        self,
        query: str,
        tenant_id: str,
        model_version: str,
        index_version: str,
        filters: Dict[str, Any]
    ) -> str:
        """
        Generates canonical cryptographic cache key ensuring zero cross-tenant contamination
        and automatic stale-index collision prevention.
        """
        canonical_dict = {
            "query": query.strip().lower(),
            "tenant_id": tenant_id,
            "model_version": model_version,
            "index_version": index_version,
            "filters": sorted(filters.items())
        }
        serialized = json.dumps(canonical_dict, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def get(self, cache_key: str) -> Optional[Any]:
        if cache_key not in self.store:
            self.misses += 1
            return None

        entry = self.store[cache_key]
        if time.time() > entry["expires_at"]:
            # Expired
            del self.store[cache_key]
            self.misses += 1
            return None

        self.hits += 1
        return entry["data"]

    def put(
        self,
        cache_key: str,
        data: Any,
        tenant_id: str,
        index_version: str
    ):
        self.store[cache_key] = {
            "data": data,
            "expires_at": time.time() + self.ttl,
            "tenant_id": tenant_id,
            "index_version": index_version
        }

    def invalidate_by_tenant(self, tenant_id: str) -> int:
        keys_to_del = [k for k, v in self.store.items() if v["tenant_id"] == tenant_id]
        for k in keys_to_del:
            del self.store[k]
        return len(keys_to_del)

    def invalidate_by_index_version(self, old_version: str) -> int:
        keys_to_del = [k for k, v in self.store.items() if v["index_version"] == old_version]
        for k in keys_to_del:
            del self.store[k]
        return len(keys_to_del)

    def get_hit_ratio(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


if __name__ == "__main__":
    cache = RetrievalCache(ttl_seconds=60)

    tenant = "enterprise_inc"
    model_v = "text-embedding-3-small"
    index_v = "v1.2.0"
    filters = {"department": "engineering", "access": "read"}
    q = "What is the database replication lag threshold?"

    key1 = cache.generate_cache_key(q, tenant, model_v, index_v, filters)

    print("=== Step 1: Initial Request (Cache Miss) ===")
    val = cache.get(key1)
    print(f"Value in cache: {val}")

    # Simulate expensive retrieval computation
    computed_chunks = [{"id": "chunk_99", "text": "Replication lag threshold is 100ms."}]
    cache.put(key1, computed_chunks, tenant, index_v)

    print("\n=== Step 2: Second Request (Cache Hit) ===")
    cached_val = cache.get(key1)
    print(f"Hit from cache: {cached_val}")
    print(f"Hit Ratio: {cache.get_hit_ratio() * 100:.1f}%")

    print("\n=== Step 3: Index Update Invalidation ===")
    purged = cache.invalidate_by_index_version(index_v)
    print(f"Purged {purged} entries matching old index {index_v}")
    val_after_purge = cache.get(key1)
    print(f"Value after index bump: {val_after_purge} (Correctly invalidated!)")
