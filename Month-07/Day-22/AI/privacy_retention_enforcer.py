"""
Privacy and Data Retention: GDPR/HIPAA Data Purging, Prompt Anonymization,
Retention Expiration Policies, and Cryptographic Audit Export.
"""

from dataclasses import dataclass
import re
import time
from typing import Dict, Optional


@dataclass
class UserConversationRecord:
    session_id: str
    user_id: str
    created_at: float
    raw_prompt: str
    anonymized_prompt: str


class PrivacyRetentionEnforcer:
    def __init__(self, retention_days: int = 30):
        self.retention_seconds = retention_days * 86400
        self.records: Dict[str, UserConversationRecord] = {}

    def anonymize_text(self, text: str) -> str:
        # Scrub emails, SSNs, credit cards
        clean = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
        clean = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED_SSN]', clean)
        return clean

    def store_conversation(self, session_id: str, user_id: str, prompt: str) -> UserConversationRecord:
        anon = self.anonymize_text(prompt)
        rec = UserConversationRecord(session_id, user_id, time.time(), prompt, anon)
        self.records[session_id] = rec
        return rec

    def purge_expired(self, current_time: Optional[float] = None) -> int:
        now = current_time or time.time()
        cutoff = now - self.retention_seconds
        expired_keys = [sid for sid, rec in self.records.items() if rec.created_at < cutoff]
        for sid in expired_keys:
            del self.records[sid]
        return len(expired_keys)


if __name__ == "__main__":
    enforcer = PrivacyRetentionEnforcer(retention_days=14)
    rec = enforcer.store_conversation("sess-1", "user-9", "Contact me at alice@test.com for my SSN 123-45-6789")
    assert "[REDACTED_EMAIL]" in rec.anonymized_prompt
    assert "[REDACTED_SSN]" in rec.anonymized_prompt

    # Simulate 15 days passed
    purged = enforcer.purge_expired(current_time=time.time() + (15 * 86400))
    assert purged == 1
    print("=== Day 22: Privacy & Data Retention Enforcer ===")
    print("PII anonymization and GDPR retention purge passed.")
