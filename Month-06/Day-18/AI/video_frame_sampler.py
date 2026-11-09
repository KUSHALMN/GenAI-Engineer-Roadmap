"""
Video Understanding Fundamentals & Dynamic Frame Sampler.
Extracts uniform and scene-change keyframes, aligns audio timestamps,
and generates timestamped video clip summaries.
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class VideoFrame:
    frame_index: int
    timestamp_sec: float
    is_keyframe: bool
    summary_description: str


class VideoFrameSampler:
    def sample_keyframes(self, duration_sec: float, fps: float = 1.0) -> List[VideoFrame]:
        frames = []
        total_frames = int(duration_sec * fps)
        for i in range(total_frames):
            ts = i / fps
            # Simulate keyframe detection on scene cuts every 4 seconds
            is_key = (i % 4 == 0) or (i == 0)
            desc = f"Scene transition at {ts:.1f}s: speaker presentation slides" if is_key else f"Sub-frame at {ts:.1f}s"
            frames.append(VideoFrame(i, ts, is_key, desc))
        return frames


if __name__ == "__main__":
    sampler = VideoFrameSampler()
    frames = sampler.sample_keyframes(duration_sec=12.0, fps=1.0)
    print("=== Video Frame Sampling & Scene Detection ===")
    for f in frames:
        if f.is_keyframe:
            print(f"Keyframe @ {f.timestamp_sec:>4.1f}s: {f.summary_description}")
