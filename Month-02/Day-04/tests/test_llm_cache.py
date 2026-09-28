"""
test_llm_cache.py — Unit tests for LLMCache TTL, keying, eviction, and stats.
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

import pytest
from llm_cache import LLMCache


def test_cache_miss_on_empty():
    cache = LLMCache()
    assert cache.get("hello", "llama3", 0.0) is None


def test_cache_set_and_get():
    cache = LLMCache()
    cache.set("hello", "llama3", "Hi there!", 0.0)
    assert cache.get("hello", "llama3", 0.0) == "Hi there!"


def test_cache_hit_increments_stats():
    cache = LLMCache()
    cache.set("q", "model", "answer", 0.0)
    cache.get("q", "model", 0.0)
    cache.get("q", "model", 0.0)
    assert cache.total_hits == 2
    assert cache.total_misses == 0


def test_cache_miss_increments_stats():
    cache = LLMCache()
    cache.get("unknown", "model", 0.0)
    assert cache.total_misses == 1
    assert cache.total_hits == 0


def test_ttl_expiry():
    cache = LLMCache(default_ttl=0.1)
    cache.set("q", "model", "answer", 0.0)
    time.sleep(0.15)
    assert cache.get("q", "model", 0.0) is None


def test_different_temperatures_different_keys():
    cache = LLMCache()
    cache.set("q", "model", "deterministic", 0.0)
    cache.set("q", "model", "creative", 1.0)
    assert cache.get("q", "model", 0.0) == "deterministic"
    assert cache.get("q", "model", 1.0) == "creative"


def test_different_models_different_keys():
    cache = LLMCache()
    cache.set("q", "llama3", "llama answer", 0.0)
    cache.set("q", "mixtral", "mixtral answer", 0.0)
    assert cache.get("q", "llama3", 0.0) == "llama answer"
    assert cache.get("q", "mixtral", 0.0) == "mixtral answer"


def test_hit_rate_calculation():
    cache = LLMCache()
    cache.set("q", "model", "ans", 0.0)
    cache.get("q", "model", 0.0)
    cache.get("miss", "model", 0.0)
    assert cache.hit_rate == 0.5


def test_max_size_eviction():
    cache = LLMCache(max_size=3)
    for i in range(4):
        cache.set(f"q{i}", "model", f"ans{i}", 0.0)
    assert len(cache._store) <= 3


def test_whitespace_normalization():
    cache = LLMCache()
    cache.set("  hello  ", "model", "answer", 0.0)
    assert cache.get("hello", "model", 0.0) == "answer"
