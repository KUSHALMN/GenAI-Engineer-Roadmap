"""
Speech-to-Text (STT) Integration & Word-Level Timestamp Transcriber.
Simulates automatic speech recognition with word alignment, speaker tags,
confidence metrics, and silence hallucination filtering.
"""

from dataclasses import dataclass
import time
from typing import List


@dataclass
class WordTimestamp:
    word: str
    start: float
    end: float
    confidence: float
    speaker: str = "speaker_0"


@dataclass
class TranscriptionSegment:
    segment_id: int
    text: str
    start: float
    end: float
    words: List[WordTimestamp]
    speaker: str = "speaker_0"


@dataclass
class TranscriptionResult:
    language: str
    duration_seconds: float
    full_text: str
    segments: List[TranscriptionSegment]
    average_confidence: float


class SpeechToTextTranscriber:
    """Simulates production ASR with word-level timestamps and hallucination filtering."""

    def __init__(self, model_size: str = "whisper-large-v3"):
        self.model_size = model_size

    def transcribe(self, audio_path: str, filter_hallucinations: bool = True) -> TranscriptionResult:
        start_time = time.perf_counter()

        # Simulated high-fidelity alignment data
        words_seg1 = [
            WordTimestamp("Welcome", 0.12, 0.54, 0.98, "speaker_1"),
            WordTimestamp("to", 0.55, 0.68, 0.99, "speaker_1"),
            WordTimestamp("the", 0.69, 0.82, 0.97, "speaker_1"),
            WordTimestamp("multimodal", 0.85, 1.42, 0.96, "speaker_1"),
            WordTimestamp("engineering", 1.44, 2.15, 0.98, "speaker_1"),
            WordTimestamp("masterclass.", 2.18, 2.95, 0.97, "speaker_1")
        ]
        seg1 = TranscriptionSegment(1, "Welcome to the multimodal engineering masterclass.", 0.12, 2.95, words_seg1, "speaker_1")

        words_seg2 = [
            WordTimestamp("Today", 3.40, 3.82, 0.96, "speaker_2"),
            WordTimestamp("we", 3.84, 4.02, 0.99, "speaker_2"),
            WordTimestamp("benchmark", 4.05, 4.65, 0.95, "speaker_2"),
            WordTimestamp("Whisper", 4.70, 5.20, 0.99, "speaker_2"),
            WordTimestamp("latency.", 5.22, 5.85, 0.96, "speaker_2")
        ]
        seg2 = TranscriptionSegment(2, "Today we benchmark Whisper latency.", 3.40, 5.85, words_seg2, "speaker_2")

        segments = [seg1, seg2]

        # Potential hallucination segment on silence (e.g. repetitive 'Thank you' or subtitle credits)
        hallucinated_words = [
            WordTimestamp("Thank", 6.10, 6.40, 0.42, "speaker_1"),
            WordTimestamp("you.", 6.42, 6.80, 0.38, "speaker_1")
        ]
        hallucinated_seg = TranscriptionSegment(3, "Thank you.", 6.10, 6.80, hallucinated_words, "speaker_1")

        if not filter_hallucinations:
            segments.append(hallucinated_seg)

        all_words = [w for s in segments for w in s.words]
        mean_conf = sum(w.confidence for w in all_words) / max(1, len(all_words))
        full_text = " ".join(s.text for s in segments)

        return TranscriptionResult(
            language="en",
            duration_seconds=6.0,
            full_text=full_text,
            segments=segments,
            average_confidence=round(mean_conf, 4)
        )

    def export_srt(self, result: TranscriptionResult) -> str:
        lines = []
        for s in result.segments:
            lines.append(str(s.segment_id))
            lines.append(f"{self._format_ts(s.start)} --> {self._format_ts(s.end)}")
            lines.append(f"[{s.speaker}] {s.text}\n")
        return "\n".join(lines)

    @staticmethod
    def _format_ts(seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"


if __name__ == "__main__":
    stt = SpeechToTextTranscriber()
    res = stt.transcribe("keynote.wav", filter_hallucinations=True)

    print("=== Transcription Result ===")
    print(f"Language: {res.language} | Confidence: {res.average_confidence}")
    print(f"Full Text: {res.full_text}\n")
    print("SRT Subtitles Export:\n")
    print(stt.export_srt(res))
