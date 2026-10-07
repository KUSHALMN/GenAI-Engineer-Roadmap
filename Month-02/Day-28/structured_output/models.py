"""Pydantic-style data models and schemas for structured outputs."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class UserProfile:
    name: str
    age: int
    interests: List[str]
    email: Optional[str] = None


@dataclass
class ExtractedActionItem:
    task: str
    assignee: str
    priority: str  # LOW, MEDIUM, HIGH, CRITICAL
    due_date: Optional[str] = None


@dataclass
class MeetingMinutes:
    topic: str
    summary: str
    action_items: List[ExtractedActionItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
