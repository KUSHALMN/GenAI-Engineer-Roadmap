# 🎯 Technical Interview Questions — Day 28: Chaos Engineering & Concurrency

### 1. What is Chaos Engineering (e.g., Netflix Chaos Monkey), and why is it vital for cloud microservices?
**Answer:**
Chaos Engineering intentionally introduces turbulent conditions (e.g., killing random server instances, injecting network packet loss, simulating third-party API 500s) into staging and production environments to verify that automatic failovers, circuit breakers, and degraded fallback modes behave as architected before real incidents occur.

### 2. Why is `computeIfAbsent()` preferred over `putIfAbsent()` on ConcurrentHashMap?
**Answer:**
`putIfAbsent(key, new AtomicLong(0))` always instantiates a new `AtomicLong` object on the heap even when the key already exists, increasing GC memory pressure. `computeIfAbsent(key, k -> new AtomicLong(0))` lazily evaluates the lambda only when the key is genuinely absent.
