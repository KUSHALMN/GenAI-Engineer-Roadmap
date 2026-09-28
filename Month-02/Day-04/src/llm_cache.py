"""
llm_cache.py — In-memory LLM response cache with TTL + SHA-256 keying.
Topic: Month 02, Day 04 — LLM Caching & Cost Optimization
"""
import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CacheEntry:
    response: str
    created_at: float
    ttl: float
    hits: int = 0

    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl


class LLMCache:
    def __init__(self, default_ttl: float = 3600.0, max_size: int = 1000):
        self._store: dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.total_hits = 0
        self.total_misses = 0

    def _make_key(self, prompt: str, model: str, temperature: float) -> str:
        payload = json.dumps(
            {"prompt": prompt.strip(), "model": model, "temperature": temperature},
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()

    def get(self, prompt: str, model: str, temperature: float = 0.0) -> Optional[str]:
        key = self._make_key(prompt, model, temperature)
        entry = self._store.get(key)
        if entry is None or entry.is_expired():
            if entry:
                del self._store[key]
            self.total_misses += 1
            return None
        entry.hits += 1
        self.total_hits += 1
        return entry.response

    def set(self, prompt: str, model: str, response: str, temperature: float = 0.0, ttl: Optional[float] = None):
        if len(self._store) >= self.max_size:
            self._evict()
        key = self._make_key(prompt, model, temperature)
        self._store[key] = CacheEntry(
            response=response,
            created_at=time.time(),
            ttl=ttl or self.default_ttl,
        )

    def _evict(self):
        # Remove all expired entries first
        expired = [k for k, v in self._store.items() if v.is_expired()]
        for k in expired:
            del self._store[k]
        # If still over limit, remove least recently used (lowest hits)
        if len(self._store) >= self.max_size:
            lru_key = min(self._store, key=lambda k: self._store[k].hits)
            del self._store[lru_key]

    @property
    def hit_rate(self) -> float:
        total = self.total_hits + self.total_misses
        return round(self.total_hits / total, 4) if total else 0.0

    @property
    def stats(self) -> dict:
        return {
            "size": len(self._store),
            "hits": self.total_hits,
            "misses": self.total_misses,
            "hit_rate": self.hit_rate,
        }
