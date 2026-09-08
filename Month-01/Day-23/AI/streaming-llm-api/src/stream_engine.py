import asyncio
import time
import uuid
from typing import AsyncGenerator, Optional, Tuple

try:
    from .schemas import StreamRequest, StreamTokenPayload, StreamMetrics
except ImportError:
    from schemas import StreamRequest, StreamTokenPayload, StreamMetrics

class StreamingLLMEngine:
    SAMPLE_RESPONSES = [
        "In production GenAI systems, streaming minimizes perceived user latency by pushing tokens immediately over Server-Sent Events (SSE) or WebSockets.",
        "Async architectures decouple network I/O from compute-intensive LLM inferences, allowing a single FastAPI worker to handle thousands of concurrent streams.",
        "Backpressure management is critical when client consumption rates drop below generation rates, preventing buffer overflow and memory bloat.",
        "Time To First Token (TTFT) is the primary metric for interactive user experience, while tokens-per-second (TPS) determines reading continuity."
    ]

    def __init__(self):
        self._request_counter = 0

    def _select_content(self, prompt: str) -> str:
        idx = hash(prompt) % len(self.SAMPLE_RESPONSES)
        base = self.SAMPLE_RESPONSES[idx]
        return f"Response to '{prompt}': {base} [Engine: AsyncStream-v1.0]"

    async def generate_stream(
        self, request: StreamRequest
    ) -> AsyncGenerator[Tuple[StreamTokenPayload, Optional[StreamMetrics]], None]:
        request_id = str(uuid.uuid4())[:8]
        full_text = self._select_content(request.prompt)
        words = full_text.split(" ")
        
        start_time = time.perf_counter()
        ttft: Optional[float] = None
        delay_sec = request.chunk_delay_ms / 1000.0

        for idx, word in enumerate(words):
            token = word + (" " if idx < len(words) - 1 else "")
            
            if idx == 0:
                await asyncio.sleep(max(0.02, delay_sec))
                ttft = (time.perf_counter() - start_time) * 1000.0
            else:
                await asyncio.sleep(delay_sec)

            is_last = (idx == len(words) - 1)
            payload = StreamTokenPayload(
                id=request_id,
                token=token,
                index=idx,
                is_finished=is_last,
                finish_reason="stop" if is_last else None
            )

            metrics = None
            if is_last:
                total_duration_ms = (time.perf_counter() - start_time) * 1000.0
                prompt_tokens = max(1, len(request.prompt) // 4)
                completion_tokens = len(words)
                tps = (completion_tokens / (total_duration_ms / 1000.0)) if total_duration_ms > 0 else 0.0

                metrics = StreamMetrics(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                    time_to_first_token_ms=round(ttft or 0.0, 2),
                    total_duration_ms=round(total_duration_ms, 2),
                    tokens_per_second=round(tps, 2)
                )

            yield payload, metrics
