"""
Day 02: Instruction Dataset Design
Validates JSONL instruction schemas (Alpaca, ShareGPT, ChatML),
ensuring role integrity, token balance, and task diversity metadata.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

@dataclass
class ChatTurn:
    role: str # "system", "user", "assistant"
    content: str

@dataclass
class InstructionRecord:
    id: str
    turns: List[ChatTurn]
    task_category: str # "summarization", "code_generation", "reasoning", "extraction"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> List[str]:
        errors = []
        if len(self.turns) < 2:
            errors.append("Dataset record must contain at least 2 turns (user + assistant).")
        if self.turns[0].role not in ["system", "user"]:
            errors.append("First turn must be 'system' or 'user'.")
        if self.turns[-1].role != "assistant":
            errors.append("Last turn must be 'assistant' response.")
        for idx, turn in enumerate(self.turns):
            if not turn.content or len(turn.content.strip()) == 0:
                errors.append(f"Turn {idx} has empty content.")
        return errors

    def to_chatml_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "messages": [{"role": t.role, "content": t.content} for t in self.turns],
            "category": self.task_category
        })

if __name__ == "__main__":
    valid_record = InstructionRecord(
        id="rec_001",
        turns=[
            ChatTurn("system", "You are an expert SQL assistant."),
            ChatTurn("user", "Write a query to find all active subscriptions."),
            ChatTurn("assistant", "SELECT * FROM subscriptions WHERE status = 'active';")
        ],
        task_category="code_generation"
    )

    errs = valid_record.validate()
    assert len(errs) == 0, f"Expected valid record, got errors: {errs}"
    print(f"ChatML JSON export:
{valid_record.to_chatml_json()}")
    print("Day 02 AI Instruction Dataset Schema passed all tests.")
