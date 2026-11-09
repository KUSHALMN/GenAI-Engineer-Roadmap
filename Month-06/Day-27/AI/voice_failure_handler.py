"""
Voice UX and Failure Handling Engine.
Handles silence timeouts, ambient background noise, low-confidence transcription,
and user interruptions with conversational fallback prompts.
"""

from dataclasses import dataclass


@dataclass
class FailureHandlingDecision:
    error_type: str
    reprompt_text: str
    escalate_to_screen: bool
    should_retry: bool


class VoiceFailureHandler:
    def handle_error(self, error_event: str, failure_count: int) -> FailureHandlingDecision:
        if error_event == "silence_timeout":
            if failure_count == 1:
                return FailureHandlingDecision(error_event, "I didn't hear anything. Are you still there?", False, True)
            else:
                return FailureHandlingDecision(error_event, "Closing session due to inactivity. Feel free to tap the mic when ready.", True, False)

        elif error_event == "low_confidence_transcription":
            return FailureHandlingDecision(error_event, "I didn't quite catch that. Could you please rephrase?", False, True)

        elif error_event == "acoustic_noise_overload":
            return FailureHandlingDecision(error_event, "It sounds a bit noisy here. Please speak closer to your microphone.", False, True)

        return FailureHandlingDecision("unknown_failure", "An unexpected error occurred. Please try again.", True, False)


if __name__ == "__main__":
    handler = VoiceFailureHandler()
    print("=== Voice UX Failure Handling Scenarios ===")
    d1 = handler.handle_error("silence_timeout", failure_count=1)
    print(f"Silence 1st try: '{d1.reprompt_text}' | Retry: {d1.should_retry}")

    d2 = handler.handle_error("silence_timeout", failure_count=2)
    print(f"Silence 2nd try: '{d2.reprompt_text}' | Escalate: {d2.escalate_to_screen}")

    d3 = handler.handle_error("low_confidence_transcription", failure_count=1)
    print(f"Low Confidence: '{d3.reprompt_text}'")
