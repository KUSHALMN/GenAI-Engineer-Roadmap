"""
Real-Time Audio Streaming Session Manager.
Manages bidirectional WebSocket sessions, partial audio chunk buffering,
live streaming transcription, and user interruption (barge-in) cancellation.
"""

from dataclasses import dataclass, field
from enum import Enum
import time
from typing import Any, Dict, List, Optional, Tuple


class SessionState(Enum):
    CONNECTED = "connected"
    LISTENING = "listening"
    USER_SPEAKING = "user_speaking"
    AGENT_RESPONDING = "agent_responding"
    INTERRUPTED = "interrupted"
    DISCONNECTED = "disconnected"


@dataclass
class AudioStreamFrame:
    session_id: str
    frame_seq: int
    audio_bytes: bytes
    is_speech: bool
    timestamp_ms: float


class AudioStreamingSession:
    """Simulates real-time full-duplex conversational voice sessions."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.state = SessionState.CONNECTED
        self.audio_buffer = bytearray()
        self.partial_transcripts: List[str] = []
        self.is_agent_speaking = False
        self.interruption_events = 0

    def start_listening(self):
        self.state = SessionState.LISTENING

    def receive_audio_frame(self, frame: AudioStreamFrame) -> Dict[str, Any]:
        if self.state == SessionState.DISCONNECTED:
            raise RuntimeError("Cannot process frames on disconnected session.")

        # Check for user barge-in (interruption)
        if self.is_agent_speaking and frame.is_speech:
            self.state = SessionState.INTERRUPTED
            self.is_agent_speaking = False
            self.interruption_events += 1
            return {
                "event": "barge_in_detected",
                "action": "cancel_agent_playback_and_clear_buffer",
                "seq": frame.frame_seq
            }

        if frame.is_speech:
            self.state = SessionState.USER_SPEAKING
            self.audio_buffer.extend(frame.audio_bytes)
            # Simulate real-time streaming partial transcript
            partial_text = f"User speech streaming chunk {frame.frame_seq}..."
            self.partial_transcripts.append(partial_text)
            return {
                "event": "partial_transcript",
                "partial_text": partial_text,
                "buffered_bytes": len(self.audio_buffer)
            }
        else:
            if self.state == SessionState.USER_SPEAKING:
                # Silence after speech -> End of turn detected
                self.state = SessionState.AGENT_RESPONDING
                self.is_agent_speaking = True
                final_text = " ".join(self.partial_transcripts)
                self.partial_transcripts.clear()
                self.audio_buffer.clear()
                return {
                    "event": "endpoint_detected",
                    "final_transcript": final_text,
                    "action": "trigger_llm_inference"
                }

        return {"event": "ambient_silence", "state": self.state.value}


if __name__ == "__main__":
    session = AudioStreamingSession("sess-m06-d13-alpha")
    session.start_listening()
    print(f"Session {session.session_id} initialized in state: {session.state.value}")

    # Simulate user speaking 3 frames
    for i in range(1, 4):
        f = AudioStreamFrame("sess-m06-d13-alpha", i, b"\x01\x02" * 160, is_speech=True, timestamp_ms=i * 20.0)
        res = session.receive_audio_frame(f)
        print(f"Frame #{i} -> {res['event']}: {res.get('partial_text', '')}")

    # User pauses -> endpointing
    pause_frame = AudioStreamFrame("sess-m06-d13-alpha", 4, b"\x00" * 160, is_speech=False, timestamp_ms=80.0)
    res_pause = session.receive_audio_frame(pause_frame)
    print(f"Frame #4 -> {res_pause['event']}: state is now {session.state.value}")

    # Agent is responding, but user speaks again -> Barge-in!
    barge_frame = AudioStreamFrame("sess-m06-d13-alpha", 5, b"\xff" * 160, is_speech=True, timestamp_ms=100.0)
    res_barge = session.receive_audio_frame(barge_frame)
    print(f"Frame #5 -> {res_barge['event']}: {res_barge['action']}")
