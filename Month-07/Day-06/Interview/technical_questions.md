# 🎯 Technical Interview Questions — Day 06: Redis & Java NIO

### 1. How do you prevent Cache Stampede (Thundering Herd) when a high-traffic cache key expires?
**Answer:**
1. **Mutex Lock (Distributed Locking):** When a cache miss occurs, the first worker acquires a Redis lock to query the DB and update the cache. Other workers wait or return stale data.
2. **Probabilistic Early Expiration (XFetch algorithm):** Keys are asynchronously refreshed in the background before they actually expire based on access frequency and DB query cost.
3. **Stale-While-Revalidate:** Return cached content immediately while a background thread updates the data.

### 2. Explain how Java NIO Channels & ByteBuffers differ from standard Java I/O Streams.
**Answer:**
Standard Java I/O (`InputStream`/`OutputStream`) is stream-oriented and blocking; you read one or more bytes at a time directly into memory. Java NIO is buffer-oriented and non-blocking: data is read into a `ByteBuffer` from a `Channel`. Buffers can be flipped, rewound, and directly mapped to OS kernel memory (DirectByteBuffer) allowing zero-copy transfers (`transferTo`).
