# Technical Interview Preparation — API Design & Bit Manipulation
1. Multipart Upload vs SSE Streaming in Multimodal APIs: Media ingestion uses multipart `POST /v1/media/upload` returning pre-signed blob pointers; query responses use W3C Server-Sent Events (SSE) `text/event-stream` for progressive token and audio playback.
2. Brian Kernighan's Algorithm: `n & (n - 1)` clears the lowest set bit in $O(\text{set bits})$ iterations.
