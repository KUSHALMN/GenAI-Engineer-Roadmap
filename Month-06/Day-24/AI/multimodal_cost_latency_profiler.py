"""
Multimodal Cost and Latency Profiler Engine.
Computes monetary cost, GPU memory (VRAM), and latency trade-offs
across image resolutions, audio durations, and video frame rates.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ModalityCostEstimate:
    modality: str
    input_units: str
    tokens: int
    cost_usd: float
    latency_est_ms: float


class MultimodalCostLatencyProfiler:
    def profile_request(self, text_words: int, image_count: int, audio_seconds: float, video_seconds: float) -> List[ModalityCostEstimate]:
        estimates = []
        # Text
        text_tokens = int(text_words * 1.33)
        estimates.append(ModalityCostEstimate("Text Prompt", f"{text_words} words", text_tokens, (text_tokens / 1e6) * 2.50, 45.0))
        # Images (High Detail 1080p -> ~1105 tokens each)
        img_tokens = image_count * 1105
        estimates.append(ModalityCostEstimate("Images (High Detail)", f"{image_count} images", img_tokens, (img_tokens / 1e6) * 2.50, image_count * 120.0))
        # Audio (12.5 tokens/sec)
        audio_tokens = int(audio_seconds * 12.5)
        estimates.append(ModalityCostEstimate("Audio", f"{audio_seconds:.1f}s audio", audio_tokens, (audio_tokens / 1e6) * 3.00, audio_seconds * 25.0))
        # Video (1 FPS -> 85 tokens/sec)
        video_tokens = int(video_seconds * 85)
        estimates.append(ModalityCostEstimate("Video (1 FPS)", f"{video_seconds:.1f}s clip", video_tokens, (video_tokens / 1e6) * 3.00, video_seconds * 60.0))

        return estimates


if __name__ == "__main__":
    profiler = MultimodalCostLatencyProfiler()
    costs = profiler.profile_request(text_words=150, image_count=2, audio_seconds=15.0, video_seconds=30.0)
    print("=== Multimodal Cost & Latency Profiling Report ===")
    total_cost = sum(c.cost_usd for c in costs)
    total_tokens = sum(c.tokens for c in costs)
    for c in costs:
        print(f" - {c.modality:<20} ({c.input_units:<12}): {c.tokens:>5} tokens | ${c.cost_usd:.6f} | ~{c.latency_est_ms:>6.1f} ms")
    print(f"Total Tokens: {total_tokens} | Total Cost: ${total_cost:.6f}")
