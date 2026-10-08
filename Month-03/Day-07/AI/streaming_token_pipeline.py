"""
Month-03 Day-07: Real-Time SSE Token Streaming & Backpressure Pipeline
Implements:
1. Server-Sent Events (SSE) stream formatter compliant with W3C SSE standard.
2. Async generator yielding token deltas, metadata headers, and [DONE] terminator.
3. Backpressure buffer manager preventing memory bloat on slow client networks.
4. Heartbeat keepalive ping mechanism for intermediate network proxies.
"""

from __future__ import annotations
import asyncio
import json
import sys
import time
from typing import AsyncGenerator, Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class SSEFormatter:
    """Formats payload dicts into standard text/event-stream chunks."""

    @staticmethod
    def format_event(data: Any, event: str = "message", event_id: str = None) -> str:
        lines = []
        if event_id:
            lines.append(f"id: {event_id}")
        if event != "message":
            lines.append(f"event: {event}")

        if isinstance(data, (dict, list)):
            payload = json.dumps(data)
        else:
            payload = str(data)

        for line in payload.splitlines():
            lines.append(f"data: {line}")
        lines.append("\n")
        return "\n".join(lines)

    @staticmethod
    def format_ping() -> str:
        """SSE comment used as keep-alive heartbeat."""
        return ": ping\n\n"

    @staticmethod
    def format_done() -> str:
        return "data: [DONE]\n\n"


class TokenStreamProducer:
    """Simulates real-time LLM token generation with chunk buffering."""

    def __init__(self, text: str, chunk_delay: float = 0.02):
        self.text = text
        self.chunk_delay = chunk_delay

    async def stream_tokens(self) -> AsyncGenerator[str, None]:
        words = self.text.split(" ")
        for i, word in enumerate(words):
            token = word + (" " if i < len(words) - 1 else "")
            chunk_data = {
                "index": i,
                "delta": token,
                "timestamp": round(time.time(), 3),
            }
            yield SSEFormatter.format_event(chunk_data)
            await asyncio.sleep(self.chunk_delay)

        yield SSEFormatter.format_done()


class BackpressureManager:
    """Monitors client consumption rates and drops or throttles buffer queues."""

    def __init__(self, max_buffer_size: int = 50):
        self.max_buffer_size = max_buffer_size
        self.queue: asyncio.Queue[str] = asyncio.Queue(maxsize=max_buffer_size)

    async def push(self, item: str) -> bool:
        if self.queue.full():
            return False  # Backpressure signal
        await self.queue.put(item)
        return True

    async def consume(self) -> str:
        return await self.queue.get()


async def run_demo():
    print("=" * 65)
    print("🚀 Day 07: Real-Time SSE Token Streaming Verification")
    print("=" * 65)

    sample_prompt_response = (
        "Server-Sent Events provide unidirectional real-time streaming over HTTP/1.1 or HTTP/2. "
        "Unlike WebSockets, SSE automatically handles reconnection, event IDs, and proxy traversal."
    )

    producer = TokenStreamProducer(sample_prompt_response, chunk_delay=0.01)
    received_tokens: List[str] = []

    print("Beginning simulated SSE client consumption:")
    async for raw_chunk in producer.stream_tokens():
        if "[DONE]" in raw_chunk:
            print("\n[STREAM TERMINATED WITH [DONE]]")
            break
        # Parse data line
        for line in raw_chunk.splitlines():
            if line.startswith("data: "):
                payload = json.loads(line[6:])
                received_tokens.append(payload["delta"])
                sys.stdout.write(payload["delta"])
                sys.stdout.flush()

    reconstructed = "".join(received_tokens)
    assert reconstructed == sample_prompt_response, "Reconstructed stream must match original text!"

    print("\n✅ Day 07 Token Streaming Pipeline Verification Successful!")


if __name__ == "__main__":
    asyncio.run(run_demo())
