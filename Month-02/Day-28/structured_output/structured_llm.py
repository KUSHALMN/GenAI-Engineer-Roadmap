"""Structured LLM generator enforcing JSON schema adherence."""
import json
from typing import Dict, Any, Tuple
from .validator import OutputValidator
from .models import MeetingMinutes, ExtractedActionItem


class StructuredLLM:
    """Wrapper that prompts model for JSON and validates against schema models."""

    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name

    def extract_meeting_minutes(self, raw_notes: str) -> MeetingMinutes:
        """Extract structured meeting minutes from unorganized transcripts."""
        # Simulated high-fidelity structured generation
        mock_response = """
        ```json
        {
            "topic": "GenAI Architecture Review",
            "summary": "Discussed prompt security, token budget latency, and structured outputs.",
            "action_items": [
                {
                    "task": "Implement regex sanitizer",
                    "assignee": "Alice",
                    "priority": "HIGH",
                    "due_date": "2026-10-15"
                },
                {
                    "task": "Setup Trie autocomplete benchmark",
                    "assignee": "Bob",
                    "priority": "MEDIUM",
                    "due_date": "2026-10-18"
                }
            ]
        }
        ```
        """
        validated_dict = OutputValidator.parse_and_validate(
            mock_response,
            required_keys=("topic", "summary", "action_items")
        )

        items = [
            ExtractedActionItem(
                task=item["task"],
                assignee=item["assignee"],
                priority=item["priority"],
                due_date=item.get("due_date")
            )
            for item in validated_dict["action_items"]
        ]

        return MeetingMinutes(
            topic=validated_dict["topic"],
            summary=validated_dict["summary"],
            action_items=items
        )
