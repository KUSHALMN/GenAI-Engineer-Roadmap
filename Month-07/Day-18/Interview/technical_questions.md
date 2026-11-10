# 🎯 Technical Interview Questions — Day 18: OpenTelemetry & LRU Cache LLD

### 1. Explain the W3C Trace Context standard (`traceparent` header).
**Answer:**
The `traceparent` HTTP header standardizes distributed trace propagation across heterogeneous microservices:
`version-traceid-parentid-traceflags` (e.g., `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`).
- `traceid`: 16-byte unique identifier linking all spans across the entire distributed request lifecycle.
- `parentid`: 8-byte identifier identifying the immediate upstream caller span.
- `traceflags`: Bitmask controlling sampling decisions (`01` = sampled for storage).

### 2. Why is a Doubly Linked List paired with a HashMap required for $O(1)$ LRU Cache operations?
**Answer:**
A HashMap provides $O(1)$ key lookup. However, array or singly-linked list removal takes $O(N)$ time. A doubly-linked list allows moving a recently accessed node to the front or removing the least recently used node from the tail in $O(1)$ pointer manipulations.
