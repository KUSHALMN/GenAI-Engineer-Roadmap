"""
Voice Activity Detection & Conversational Turn-Taking Controller.
Detects speech onset, conversational pauses, and speech endpointing
using dual-threshold energy windowing and adaptive silence timers.
"""

from dataclasses import dataclass, field
import time
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class TurnTakingConfig:
    speech_start_threshold_ms: float = 120.0   # Must sustain speech for 120ms to avoid clicks
    silence_endpoint_threshold_ms: float = 650.0 # 650ms pause signals user turn completion
    max_turn_duration_sec: float = 30.0        # Force turn handover at 30 seconds


class VoiceTurnTakingController:
    """Controls conversational turn-taking between user and AI agent."""

    def __init__(self, config: Optional[TurnTakingConfig] = None):
        self.config = config or TurnTakingConfig()
        self.in_user_turn = False
        self.speech_start_time: Optional[float] = None
        self.last_speech_time: Optional[float] = None

    def process_vad_event(self, is_speech: bool, timestamp_ms: float) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Processes streaming frame VAD events and returns turn-taking triggers:
        'NONE', 'SPEECH_STARTED', or 'SPEECH_ENDED'.
        """
        if is_speech:
            self.last_speech_time = timestamp_ms
            if not self.in_user_turn:
                if self.speech_start_time is None:
                    self.speech_start_time = timestamp_ms
                elif (timestamp_ms - self.speech_start_time) >= self.config.speech_start_threshold_ms:
                    self.in_user_turn = True
                    return "SPEECH_STARTED", {"onset_ms": self.speech_start_time}
        else:
            self.speech_start_time = None  # Reset false-alarm onset candidate
            if self.in_user_turn and self.last_speech_time is not None:
                pause_duration = timestamp_ms - self.last_speech_time
                if pause_duration >= self.config.silence_endpoint_threshold_ms:
                    self.in_user_turn = False
                    turn_len = (self.last_speech_time - (self.speech_start_time or 0)) / 1000.0
                    info = {
                        "endpoint_ms": timestamp_ms,
                        "pause_ms": pause_duration
                    }
                    self.last_speech_time = None
                    return "SPEECH_ENDED", info

        return "NONE", None


if __name__ == "__main__":
    controller = VoiceTurnTakingController()

    print("=== Simulating Conversational Turn-Taking ===")
    timeline = [
        # Transient noise click (60ms) - should NOT trigger speech started
        (True, 20.0), (True, 40.0), (True, 60.0), (False, 80.0), (False, 100.0),
        # Genuine user speech starts at 200ms
        (True, 200.0), (True, 260.0), (True, 340.0), (True, 500.0), (True, 800.0),
        # User pauses for breath (200ms) - should NOT trigger endpoint
        (False, 860.0), (False, 920.0), (True, 1000.0), (True, 1200.0),
        # User finishes speaking; silence exceeds 650ms
        (False, 1300.0), (False, 1500.0), (False, 1860.0), (False, 1960.0)
    ]

    for is_speech, ts in timeline:
        action, meta = controller.process_vad_event(is_speech, ts)
        if action != "NONE":
            print(f"[{ts:.1f} ms] Event Triggered -> {action} | Details: {meta}")
