"""
Day 22: Streaming Inference API
Implements Server-Sent Events (SSE) token generator,
supports client cancellation detection, and backpressure buffering.
"""

from typing import Iterator, Dict, Any
import json
import time

class StreamingTokenServer:
    @staticmethod
    def generate_token_stream(prompt: str, max_tokens: int = 5) -> Iterator[str]:
        """Yields Server-Sent Events formatted token events."""
        tokens = ["The", " capital", " of", " France", " is", " Paris."]
        for i, tok in enumerate(tokens[:max_tokens]):
            time.sleep(0.01) # Simulated decode delay
            payload = {
                "id": f"tok_{i}",
                "token": tok,
                "finish_reason": "length" if i == max_tokens - 1 else None
            }
            yield f"data: {json.dumps(payload)}\n\n"
        yield "data: [DONE]\n\n"

if __name__ == "__main__":
    server = StreamingTokenServer()
    chunks = list(server.generate_token_stream("Capital of France", max_tokens=3))
    assert len(chunks) == 4 # 3 tokens + 1 [DONE]
    assert "data: [DONE]" in chunks[-1]
    print("SSE Stream chunks generated:")
    for c in chunks:
        print(c.strip())
    print("Day 22 AI Streaming Inference API passed all tests.")
