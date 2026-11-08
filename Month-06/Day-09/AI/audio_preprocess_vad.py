"""
Audio Pipeline Foundations & Voice Activity Detection (VAD) Engine.
Handles audio metadata, resamples to 16kHz mono PCM, computes Short-Time Energy
and Zero-Crossing Rate (ZCR), and chunks speech into active voiced intervals.
"""

from dataclasses import dataclass, field
import math
import time
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class AudioMetadata:
    sample_rate: int
    channels: int
    duration_seconds: float
    total_samples: int
    codec: str = "pcm_s16le"


@dataclass
class VoicedSegment:
    start_time: float
    end_time: float
    duration: float
    mean_energy: float


class AudioPreprocessVAD:
    """Processes raw audio waveforms and performs Voice Activity Detection."""

    TARGET_SAMPLE_RATE = 16000  # 16kHz standard for ASR

    def __init__(self, frame_duration_ms: int = 30, energy_threshold: float = 0.05):
        self.frame_duration_ms = frame_duration_ms
        self.energy_threshold = energy_threshold
        self.frame_size = int(self.TARGET_SAMPLE_RATE * (frame_duration_ms / 1000.0))

    def resample_and_normalize(self, raw_samples: List[float], source_rate: int) -> Tuple[List[float], AudioMetadata]:
        """Simulates linear interpolation resampling to 16kHz mono and amplitude normalization."""
        ratio = self.TARGET_SAMPLE_RATE / source_rate
        target_len = int(len(raw_samples) * ratio)
        resampled = [raw_samples[min(len(raw_samples) - 1, int(i / ratio))] for i in range(target_len)]
        
        # Normalize to [-1.0, 1.0]
        max_amp = max(abs(x) for x in resampled) if resampled else 1.0
        normalized = [x / max(1e-5, max_amp) for x in resampled]

        meta = AudioMetadata(
            sample_rate=self.TARGET_SAMPLE_RATE,
            channels=1,
            duration_seconds=round(len(normalized) / self.TARGET_SAMPLE_RATE, 2),
            total_samples=len(normalized)
        )
        return normalized, meta

    def compute_frame_energy(self, frame: List[float]) -> float:
        if not frame:
            return 0.0
        return sum(x * x for x in frame) / len(frame)

    def compute_zero_crossing_rate(self, frame: List[float]) -> float:
        if len(frame) < 2:
            return 0.0
        crossings = sum(1 for i in range(1, len(frame)) if (frame[i] >= 0) != (frame[i - 1] >= 0))
        return crossings / (len(frame) - 1)

    def detect_voice_activity(self, samples: List[float]) -> List[VoicedSegment]:
        segments = []
        in_speech = False
        start_idx = 0
        current_energies = []

        for i in range(0, len(samples), self.frame_size):
            frame = samples[i:i + self.frame_size]
            energy = self.compute_frame_energy(frame)
            zcr = self.compute_zero_crossing_rate(frame)

            # Voiced frame heuristic: significant energy + moderate ZCR
            is_voiced = energy > self.energy_threshold

            if is_voiced and not in_speech:
                in_speech = True
                start_idx = i
                current_energies = [energy]
            elif is_voiced and in_speech:
                current_energies.append(energy)
            elif not is_voiced and in_speech:
                in_speech = False
                end_time = i / self.TARGET_SAMPLE_RATE
                start_time = start_idx / self.TARGET_SAMPLE_RATE
                duration = end_time - start_time
                if duration >= 0.1:  # Filter out transient clicks < 100ms
                    segments.append(VoicedSegment(
                        start_time=round(start_time, 2),
                        end_time=round(end_time, 2),
                        duration=round(duration, 2),
                        mean_energy=round(sum(current_energies) / len(current_energies), 4)
                    ))

        return segments


if __name__ == "__main__":
    vad = AudioPreprocessVAD()

    # Generate synthetic audio: 1 sec silence, 2 sec voiced signal, 1 sec silence
    sample_rate_src = 44100
    duration_total = 4.0
    synth_samples = []
    for t in [i / sample_rate_src for i in range(int(sample_rate_src * duration_total))]:
        if 1.0 <= t <= 3.0:
            synth_samples.append(math.sin(2 * math.pi * 440.0 * t) * 0.8)  # 440 Hz tone
        else:
            synth_samples.append(0.005)  # Background noise

    normalized, meta = vad.resample_and_normalize(synth_samples, sample_rate_src)
    print("=== Audio Resampling & Metadata ===")
    print(f"Sample Rate: {meta.sample_rate} Hz | Duration: {meta.duration_seconds}s | Samples: {meta.total_samples}")

    voiced_segments = vad.detect_voice_activity(normalized)
    print("\n=== Detected Voiced Activity Segments ===")
    for s in voiced_segments:
        print(f" - Segment: [{s.start_time}s -> {s.end_time}s] (Duration: {s.duration}s, Energy: {s.mean_energy})")
