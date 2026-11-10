# 🎯 Technical Interview Questions — Day 10: Reverse Proxies & Backpressure

### 1. What is the role of a Reverse Proxy (e.g., NGINX, Envoy, Traefik) in LLM inference architectures?
**Answer:**
A reverse proxy acts as the unified frontend gateway:
- **TLS Termination:** Decrypts HTTPS at the network boundary so backend microservices communicate over fast private networks.
- **Request Buffering & SSE Streaming:** Manages slow clients without tying up GPU worker threads.
- **Header Injection & Tracing:** Injects distributed tracing headers (`traceparent`, `X-Request-ID`).
- **Load Balancing:** Distributes inference requests across multiple model serving replicas based on least-connections or active queue depths.

### 2. Why must `wait()` inside synchronized blocks always be called within a `while` loop instead of an `if` condition?
**Answer:**
To guard against **spurious wakeups** (the JVM thread waking up without an explicit `notify()`) and race conditions where another thread consumes the resource immediately after `notifyAll()` is called before the awakened thread acquires the monitor.
