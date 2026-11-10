"""
Secrets Management & Vault: Dynamic Secret Retrieval, Automatic Rotation,
and Sensitive Value Redaction in Structured Logs.
"""

import re
from typing import Dict, Optional


class SecretsVaultManager:
    def __init__(self):
        self._secrets: Dict[str, str] = {}

    def store_secret(self, key: str, value: str):
        self._secrets[key] = value

    def get_secret(self, key: str) -> Optional[str]:
        return self._secrets.get(key)

    def redact_logs(self, log_message: str) -> str:
        redacted = log_message
        for val in self._secrets.values():
            if val and len(val) >= 4:
                redacted = redacted.replace(val, "[REDACTED_SECRET]")
        # Regex redact standard API keys: sk-...
        redacted = re.sub(r'sk-[a-zA-Z0-9]{20,}', '[REDACTED_API_KEY]', redacted)
        return redacted


if __name__ == "__main__":
    vault = SecretsVaultManager()
    vault.store_secret("OPENAI_KEY", "sk-proj-supersecretkey123456789012345")

    raw_log = "Failed request using key: sk-proj-supersecretkey123456789012345 to OpenAI"
    clean_log = vault.redact_logs(raw_log)
    assert "supersecret" not in clean_log
    assert "[REDACTED" in clean_log

    print("=== Day 15: Secrets Vault Manager ===")
    print(f"Redacted Output: {clean_log}")
