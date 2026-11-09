"""
Speech-to-Speech Architecture Pipeline & Latency Profiler.
Compares Cascaded (ASR -> LLM -> TTS) vs. Native Audio-to-Audio architectures,
profiles latency across each stage, and simulates interleaved streaming buffers.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class StageLatency:
    stage_name: str
    latency_ms: float
    description: str


@dataclass
class SpeechToSpeechProfile:
    architecture: str
    total_latency_ms: float
    time_to_first_audio_ms: float
    stage_breakdown: List[StageLatency]
    pros: List[str]
    cons: List[str]


class SpeechToSpeechPipeline:
    """Profiles and simulates cascaded vs native end-to-end speech architectures."""

    @staticmethod
    def profile_cascaded_pipeline(input_audio_duration_sec: float = 3.5) -> SpeechToSpeechProfile:
        stages = [
            StageLatency("ASR (Whisper)", 180.0, "Acoustic spectrogram to text tokens"),
            StageLatency("LLM Prefill (vLLM)", 45.0, "Prompt ingestion & first token generation"),
            StageLatency("LLM Sentence Decode", 160.0, "Generates first complete response sentence"),
            StageLatency("TTS Synthesis Chunk 1", 120.0, "Converts first sentence text to 24kHz PCM audio"),
            StageLatency("Network Audio Buffering", 35.0, "WebSocket packetization & jitter buffer")
        ]

        ttfa = sum(s.latency_ms for s in stages)
        total_time = ttfa + 650.0  # Remaining sentences synthesize in background

        return SpeechToSpeechProfile(
            architecture="Cascaded (ASR -> LLM -> TTS)",
            total_latency_ms=round(total_time, 2),
            time_to_first_audio_ms=round(ttfa, 2),
            stage_breakdown=stages,
            pros=[
                "Explicit text transcript provides complete guardrails & auditability",
                "Modular: each component (Whisper, LLaMA, ElevenLabs) can be upgraded independently",
                "Cost-effective: uses standard text LLM inference backends"
            ],
            cons=[
                "Latency accumulates across three sequential stages (~540ms TTFA)",
                "Loses paralinguistic acoustic cues (tone, emotion, laughter, whisper)",
                "Errors compound: ASR transcript errors cascade into wrong LLM answers"
            ]
        )

    @staticmethod
    def profile_native_audio_pipeline() -> SpeechToSpeechProfile:
        stages = [
            StageLatency("Audio Tokenizer (e.g. SNAC / EnCodec)", 35.0, "Direct acoustic token encoding"),
            StageLatency("Native Multimodal LLM Prefill", 80.0, "Audio-to-audio cross-attention transformer"),
            StageLatency("Audio Token Autoregressive Decode", 95.0, "Predicts speech code tokens directly"),
            StageLatency("Audio Vocoder", 30.0, "Neural vocoder reconstructs raw waveform from tokens")
        ]

        ttfa = sum(s.latency_ms for s in stages)
        total_time = ttfa + 450.0

        return SpeechToSpeechProfile(
            architecture="Native Speech-to-Speech (GPT-4o Audio / Gemini Live)",
            total_latency_ms=round(total_time, 2),
            time_to_first_audio_ms=round(ttfa, 2),
            stage_breakdown=stages,
            pros=[
                "Ultra-low latency: TTFA under 250ms (human conversational speed)",
                "Preserves emotional intonation, vocal pitch, accents, and laughter",
                "Zero cascading transcription error"
            ],
            cons=[
                "Significantly harder to audit and apply text-based safety guardrails",
                "Higher training and serving compute cost per minute",
                "Vulnerable to audio-steganographic prompt injections"
            ]
        )


if __name__ == "__main__":
    pipeline = SpeechToSpeechPipeline()

    cascaded = pipeline.profile_cascaded_pipeline()
    print("=" * 60)
    print(f"=== {cascaded.architecture} ===")
    print(f"Time-to-First-Audio (TTFA): {cascaded.time_to_first_audio_ms} ms")
    for s in cascaded.stage_breakdown:
        print(f"  - {s.stage_name:<28}: {s.latency_ms:>6.1f} ms | {s.description}")

    native = pipeline.profile_native_audio_pipeline()
    print("\n" + "=" * 60)
    print(f"=== {native.architecture} ===")
    print(f"Time-to-First-Audio (TTFA): {native.time_to_first_audio_ms} ms")
    for s in native.stage_breakdown:
        print(f"  - {s.stage_name:<28}: {s.latency_ms:>6.1f} ms | {s.description}")
